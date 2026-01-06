import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# --- 페이지 설정 ---
st.set_page_config(page_title="Einstein Equivalence Principle", layout="wide")
st.title("🚀 아인슈타인 등가원리 시뮬레이션")

# --- 사이드바 설정 ---
with st.sidebar:
    st.header("⚙️ 시뮬레이션 설정")
    target = st.radio("관측 대상 선택", ["사과 (Apple)", "빛 (Light)"])
    accel = st.slider("로켓 가속도 (a)", 0.0, 10.0, 5.0)
    c_speed = 25.0 if target == "빛 (Light)" else 0
    start_btn = st.button("시뮬레이션 시작")

# --- 로켓 그리기 함수 ---
def draw_rocket(ax, y_pos, color='silver'):
    # 몸통
    rocket_body = plt.Rectangle((-2, y_pos), 4, 10, color=color, alpha=0.8, edgecolor='black')
    ax.add_patch(rocket_body)
    # 머리
    head = plt.Polygon([[-2, y_pos+10], [0, y_pos+14], [2, y_pos+10]], color='red', edgecolor='black')
    ax.add_patch(head)
    # 왼쪽 날개
    wing_l = plt.Polygon([[-2, y_pos], [-3, y_pos], [-2, y_pos+3]], color='blue', edgecolor='black')
    ax.add_patch(wing_l)
    # 오른쪽 날개 (오류 수정 지점)
    wing_r = plt.Polygon([[2, y_pos], [3, y_pos], [2, y_pos+3]], color='blue', edgecolor='black')
    ax.add_patch(wing_r)

# --- 시뮬레이션 실행 ---
if start_btn:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔭 관측자 2 (외부 관성계)")
        st.write("로켓이 가속되고, 사과는 정지하며, 빛은 직진합니다.")
        out_plot = st.empty()
    with col2:
        st.subheader("👨‍🚀 관측자 1 (로켓 내부 가속계)")
        st.write("로켓은 정지해 있고, 사과는 낙하하며, 빛은 휘어집니다.")
        in_plot = st.empty()

    t_steps = np.linspace(0, 3, 50)
    ext_light_x, ext_light_y = [], []
    int_light_x, int_light_y = [], []
    start_y = 5 

    for t in t_steps:
        y_rocket = 0.5 * accel * t**2  # 로켓의 상승 변위
        
        # --- 1. 외부 시점 (Observer 2) ---
        fig_ext, ax_ext = plt.subplots(figsize=(5, 7))
        ax_ext.set_xlim(-10, 10); ax_ext.set_ylim(-2, 55)
        draw_rocket(ax_ext, y_rocket)
        
        if target == "사과 (Apple)":
            ax_ext.plot(0, start_y + 5, 'ro', markersize=12) # 외부에선 사과가 정지(관성)
        else:
            lx_ext = c_speed * t - 5
            ly_ext = start_y + 5 # 외부에선 빛이 수평 직선
            ext_light_x.append(lx_ext)
            ext_light_y.append(ly_ext)
            ax_ext.plot(ext_light_x, ext_light_y, 'y-', lw=1, alpha=0.5)
            ax_ext.plot(lx_ext, ly_ext, 'y*', markersize=10)
        out_plot.pyplot(fig_ext)
        plt.close(fig_ext)

        # --- 2. 내부 시점 (Observer 1) ---
        fig_int, ax_int = plt.subplots(figsize=(5, 7))
        ax_int.set_xlim(-10, 10); ax_int.set_ylim(-2, 20)
        # 내부에선 로켓 벽면이 고정된 상태
        ax_int.add_patch(plt.Rectangle((-4, 0), 8, 15, color='gray', alpha=0.1, edgecolor='black'))
        
        if target == "사과 (Apple)":
            # 내부 관측자에게는 사과가 아래로 가속됨 (자유낙하)
            y_apple_int = (start_y + 5) - y_rocket
            ax_int.plot(0, max(0, y_apple_int), 'ro', markersize=12)
        else:
            # 내부 관측자에게는 빛이 아래로 휘어짐
            lx_int = c_speed * t - 5
            ly_int = (start_y + 5) - y_rocket
            int_light_x.append(lx_int)
            int_light_y.append(ly_int)
            ax_int.plot(int_light_x, int_light_y, 'y-', lw=2)
            ax_int.plot(lx_int, ly_int, 'y*', markersize=10)
        in_plot.pyplot(fig_int)
        plt.close(fig_int)
        
        time.sleep(0.03)
