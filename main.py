import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# --- 페이지 설정 ---
st.set_page_config(page_title="Einstein Equivalence Principle", layout="wide")
st.title("🚀 아인슈타인 등가원리 시뮬레이션")
st.markdown("외부에서는 직선인 빛이 가속하는 로켓 내부에서는 어떻게 휘어지는지 확인해보세요.")

# --- 사이드바 설정 ---
with st.sidebar:
    st.header("⚙️ 시뮬레이션 설정")
    target = st.radio("관측 대상 선택", ["사과 (Apple)", "빛 (Light)"])
    accel = st.slider("로켓 가속도 (a)", 0.0, 10.0, 5.0)
    if target == "빛 (Light)":
        c_speed = st.slider("빛의 상대 속도", 10.0, 50.0, 25.0)
    else:
        c_speed = 0
    
    start_btn = st.button("시뮬레이션 시작")

# --- 로켓 그리기 함수 ---
def draw_rocket(ax, y_pos, color='silver'):
    # 몸통
    rocket_body = plt.Rectangle((-2, y_pos), 4, 10, color=color, alpha=0.8, edgecolor='black')
    ax.add_patch(rocket_body)
    # 머리
    head = plt.Polygon([[-2, y_pos+10], [0, y_pos+14], [2, y_pos+10]], color='red', edgecolor='black')
    ax.add_patch(head)
    # 날개
    wing_l = plt.Polygon([[-2, y_pos], [-3, y_pos], [-2, y_pos+3]], color='blue', edgecolor='black')
    wing_r = plt.Polygon([[2, y_pos], [3, y_pos], [[2, y_pos+3]]], color='blue', edgecolor='black') # 오타수정
    ax.add_patch(wing_l)
    ax.add_patch(plt.Polygon([[2, y_pos], [3, y_pos], [2, y_pos+3]], color='blue', edgecolor='black'))

# --- 시뮬레이션 실행 ---
if start_btn:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔭 관측자 2 (외부 관성계)")
        out_plot = st.empty()
    with col2:
        st.subheader("👨‍🚀 관측자 1 (로켓 내부 가속계)")
        in_plot = st.empty()

    # 데이터 저장용 리스트 (자취 기록)
    t_steps = np.linspace(0, 3, 50)
    ext_light_x, ext_light_y = [], []
    int_light_x, int_light_y = [], []
    
    start_y = 5 # 빛/사과 시작 높이

    for t in t_steps:
        # 1. 물리 계산
        y_rocket = 0.5 * accel * t**2  # 로켓의 위치
        
        # --- 외부 시점 (Observer 2) ---
        fig_ext, ax_ext = plt.subplots(figsize=(5, 7))
        ax_ext.set_xlim(-10, 10); ax_ext.set_ylim(-2, 55)
        draw_rocket(ax_ext, y_rocket)
        
        if target == "사과 (Apple)":
            ax_ext.plot(0, start_y + 5, 'ro', markersize=12) # 공중에 멈춘 사과
        else:
            # 빛의 자취 (외부: 직선)
            curr_lx_ext = c_speed * t - 5
            curr_ly_ext = start_y # 외부에서 빛은 y축 높이 변화 없음
            ext_light_x.append(curr_lx_ext)
            ext_light_y.append(curr_ly_ext)
            ax_ext.plot(ext_light_x, ext_light_y, 'y-', lw=1, alpha=0.5) # 자취
            ax_ext.plot(curr_lx_ext, curr_ly_ext, 'y*', markersize=10) # 현재 빛 위치
            
        out_plot.pyplot(fig_ext)
        plt.close(fig_ext)

        # --- 내부 시점 (Observer 1) ---
        fig_int, ax_int = plt.subplots(figsize=(5, 7))
        ax_int.set_xlim(-10, 10); ax_int.set_ylim(-2, 20)
        # 내부에선 로켓이 고정 (배경 박스)
        ax_int.add_patch(plt.Rectangle((-4, 0), 8, 15, color='gray', alpha=0.1, edgecolor='black'))
        
        if target == "사과 (Apple)":
            y_apple_int = (start_y + 5) - y_rocket
            ax_int.plot(0, max(0, y_apple_int), 'ro', markersize=12)
        else:
            # 빛의 자취 (내부: 로켓 가속 때문에 아래로 휘어짐)
            curr_lx_int = c_speed * t - 5
            curr_ly_int = start_y - (0.5 * accel * t**2)
            int_light_x.append(curr_lx_int)
            int_light_y.append(curr_ly_int)
            ax_int.plot(int_light_x, int_light_y, 'y-', lw=2) # 휘어지는 자취
            ax_int.plot(curr_lx_int, curr_ly_int, 'y*', markersize=10)
            
        in_plot.pyplot(fig_int)
        plt.close(fig_int)
        
        time.sleep(0.03)
