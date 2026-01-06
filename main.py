import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# 실제 빛의 속도 (m/s) - 시뮬레이션 계산용
REAL_C = 299792458 

st.set_page_config(page_title="Einstein Equivalence Principle", layout="wide")
st.title("🚀 등가원리 시뮬레이션: 상대론적 속도 표현")

with st.sidebar:
    st.header("⚙️ 시뮬레이션 설정")
    target = st.radio("관측 대상 선택", ["사과 (Apple)", "빛 (Light)"])
    
    # 목표 속도 설정 (가속도를 결정하는 요인)
    target_v_c = st.slider("3초 후 도달할 로켓 속도 (단위: c)", 0.1, 0.9, 0.5)
    
    # 시뮬레이션 상의 '빛의 속도' (시각화를 위해 실제보다 매우 느리게 설정)
    # 실제 c를 쓰면 빛이 순식간에 사라지므로 시각화용 c를 따로 정의합니다.
    visual_c = 40.0 
    
    start_btn = st.button("시뮬레이션 시작")

# 로켓 가속도 계산: v = a * t => a = v / t (3초 기준)
# 시각화 공간의 크기에 맞춰 스케일링된 가속도
accel = (target_v_c * visual_c) / 3.0

def draw_rocket(ax, y_pos, color='silver'):
    rocket_body = plt.Rectangle((-2, y_pos), 4, 10, color=color, alpha=0.8, edgecolor='black')
    ax.add_patch(rocket_body)
    head = plt.Polygon([[-2, y_pos+10], [0, y_pos+14], [2, y_pos+10]], color='red', edgecolor='black')
    ax.add_patch(head)
    wing_l = plt.Polygon([[-2, y_pos], [-3, y_pos], [-2, y_pos+3]], color='blue', edgecolor='black')
    wing_r = plt.Polygon([[2, y_pos], [3, y_pos], [2, y_pos+3]], color='blue', edgecolor='black')
    ax.add_patch(wing_l)
    ax.add_patch(wing_r)

if start_btn:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔭 관측자 2 (외부 관성계)")
        out_plot = st.empty()
        out_info = st.empty()
    with col2:
        st.subheader("👨‍🚀 관측자 1 (로켓 내부 가속계)")
        in_plot = st.empty()
        in_info = st.empty()

    t_steps = np.linspace(0, 3, 60)
    ext_light_x, ext_light_y = [], []
    int_light_x, int_light_y = [], []
    start_y = 5 

    for t in t_steps:
        # 물리 계산
        current_v = accel * t
        current_v_c = current_v / visual_c  # 현재 속도를 c 단위로 환산
        y_rocket = 0.5 * accel * t**2
        
        # 정보 표시
        out_info.metric("로켓 현재 속도", f"{current_v_c:.2f} c")
        in_info.write(f"내부 관측자는 자신이 가속됨을 느끼며, 이를 **{current_v_c*10:.1f}G**의 중력으로 해석할 수 있습니다.")

        # --- 1. 외부 시점 ---
        fig_ext, ax_ext = plt.subplots(figsize=(5, 7))
        ax_ext.set_xlim(-10, 10); ax_ext.set_ylim(-2, 60)
        draw_rocket(ax_ext, y_rocket)
        
        if target == "사과 (Apple)":
            ax_ext.plot(0, start_y + 5, 'ro', markersize=12)
        else:
            lx_ext = visual_c * t - 8
            ly_ext = start_y + 5
            ext_light_x.append(lx_ext)
            ext_light_y.append(ly_ext)
            ax_ext.plot(ext_light_x, ext_light_y, 'y-', lw=1, alpha=0.5)
            ax_ext.plot(lx_ext, ly_ext, 'y*', markersize=10)
        out_plot.pyplot(fig_ext)
        plt.close(fig_ext)

        # --- 2. 내부 시점 ---
        fig_int, ax_int = plt.subplots(figsize=(5, 7))
        ax_int.set_xlim(-10, 10); ax_int.set_ylim(-2, 20)
        ax_int.add_patch(plt.Rectangle((-4, 0), 8, 15, color='gray', alpha=0.1, edgecolor='black'))
        
        if target == "사과 (Apple)":
            y_apple_int = (start_y + 5) - y_rocket
            ax_int.plot(0, max(0, y_apple_int), 'ro', markersize=12)
        else:
            lx_int = visual_c * t - 8
            ly_int = (start_y + 5) - y_rocket
            int_light_x.append(lx_int)
            int_light_y.append(ly_int)
            ax_int.plot(int_light_x, int_light_y, 'y-', lw=2)
            ax_int.plot(lx_int, ly_int, 'y*', markersize=10)
        in_plot.pyplot(fig_int)
        plt.close(fig_int)
        
        time.sleep(0.02)
