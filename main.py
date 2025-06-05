import streamlit as st
import random
import time

# 초기 상태 세팅
if "spaceship_x" not in st.session_state:
    st.session_state.spaceship_x = 250
    st.session_state.spaceship_y = 450
    st.session_state.bullets = []
    st.session_state.planets = []
    st.session_state.score = 0
    st.session_state.game_over = False

# 기본 설정
canvas_width = 600
canvas_height = 500
spaceship_speed = 20
bullet_speed = 10
planet_speed = 3

# 우주선 이동
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("⬅️"):
        st.session_state.spaceship_x = max(0, st.session_state.spaceship_x - spaceship_speed)
with col2:
    if st.button("➡️"):
        st.session_state.spaceship_x = min(canvas_width - 40, st.session_state.spaceship_x + spaceship_speed)
with col3:
    if st.button("⬆️"):
        st.session_state.spaceship_y = max(0, st.session_state.spaceship_y - spaceship_speed)
with col4:
    if st.button("⬇️"):
        st.session_state.spaceship_y = min(canvas_height - 40, st.session_state.spaceship_y + spaceship_speed)
with col5:
    if st.button("🔫"):
        # 총알 추가
        st.session_state.bullets.append({
            "x": st.session_state.spaceship_x + 15,
            "y": st.session_state.spaceship_y
