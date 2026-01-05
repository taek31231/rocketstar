import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# --- 페이지 설정 ---
st.set_page_config(page_title="Einstein Equivalence Principle", layout="wide")
st.title("🚀 아인슈타인 등가원리 시뮬레이션")
st.markdown("로켓의 가속운동이 중력과 어떻게 같은지 관찰해보세요.")

# --- 사이드바 설정 (컨트롤러) ---
with st.sidebar:
    st.header("⚙️ 시뮬레이션 설정")
    target = st.radio("관측 대상 선택", ["사과 (Apple)", "빛 (Light)"])
    accel = st.slider("로켓 가속도 (a)", 0.0, 10.0, 5.0)
    if target == "빛 (Light)":
        c_speed = st.slider("빛의 상대 속도", 10.0, 50.0, 30.0)
    else:
        c_speed = 0
    
    start_btn = st.button("시뮬레이션 시작")

# --- 시각화 함수 ---
def draw_rocket(ax, y_pos, color='silver'):
    # 로켓 몸통
    rocket_body = plt.Rectangle((-2, y_pos), 4, 10, color=color, alpha=0.8)
    # 로켓 머리 (삼각형)
    head_x = [-2, 0, 2]
    head_y = [y_pos + 10, y_pos + 14, y_pos + 10]
    # 로켓 날개
    wing_x = [-3, -2, 2, 3]
    wing_y = [y_pos, y_pos+3, y_pos+3, y_pos]
    
    ax.add_patch(rocket_body)
    ax.fill(head_x, head_y, "red")
    ax.fill(wing_x, wing_y, "blue")

# --- 시뮬레이션 로직 ---
if start_btn:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔭 관측자 2 (외부 관성계)")
        out_plot = st.empty()
    with col2:
        st.subheader("👨‍🚀 관측자 1 (로켓 내부 가속계)")
        in_plot = st.empty()

    # 데이터 초기화
    t_steps = np.linspace(0, 3, 40)
    apple_y_start = 7
    light_path_x, light_path_y = [], []

    for t in t_steps:
        # 1. 외부 좌표 계산
        y_rocket = 0.5 * accel * t**2
        y_apple_ext = apple_y_start # 외부에서 사과는 정지
        
        # 2. 내부 좌표 계산
        y_apple_int = apple_y_start - (0.5 * accel * t**2)
        
        # --- 외부 시점 그래프 ---
        fig_ext, ax_ext = plt.subplots(figsize=(5, 7))
        ax_ext.set_xlim(-10, 10); ax_ext.set_ylim(-2, 50)
        draw_rocket(ax_ext, y_rocket)
        if target == "사과 (Apple)":
            ax_ext.plot(0, y_apple_ext, 'ro', markersize=15)
        else:
            # 빛 (직선)
            lx = c_speed * t - 5
            if -2 < lx < 2: ax_ext.plot(lx, y_rocket + 5, 'y*', markersize=10)
        out_plot.pyplot(fig_ext)
        plt.close(fig_ext)

        # --- 내부 시점 그래프 ---
        fig_int, ax_int = plt.subplots(figsize=(5, 7))
        ax_int.set_xlim(-10, 10); ax_int.set_ylim(-2, 20)
        # 내부에선 로켓이 고정되어 보임 (바닥 0)
        ax_int.add_patch(plt.Rectangle((-5, 0), 10, 18, color='lightgray', alpha=0.3))
        if target == "사과 (Apple)":
            ax_int.plot(0, y_apple_int if y_apple_int > 0 else 0, 'ro', markersize=15)
        else:
            # 빛 (휘어짐)
            curr_lx = c_speed * t - 5
            curr_ly = 5 - (0.5 * accel * t**2)
            light_path_x.append(curr_lx)
            light_path_y.append(curr_ly)
            ax_int.plot(light_path_x, light_path_y, 'y-', lw=2)
            ax_int.plot(curr_lx, curr_ly, 'y*', markersize=10)
        
        in_plot.pyplot(fig_int)
        plt.close(fig_int)
        
        time.sleep(0.05)

else:
    st.info("왼쪽 사이드바에서 설정을 마친 후 '시뮬레이션 시작' 버튼을 눌러주세요.")
