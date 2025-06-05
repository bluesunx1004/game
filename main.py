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
        })

# 행성 생성
if random.random() < 0.03:
    st.session_state.planets.append({
        "x": random.randint(0, canvas_width - 40),
        "y": 0,
        "size": random.randint(20, 60)
    })

# 총알 이동
new_bullets = []
for bullet in st.session_state.bullets:
    bullet["y"] -= bullet_speed
    if bullet["y"] > 0:
        new_bullets.append(bullet)
st.session_state.bullets = new_bullets

# 행성 이동
new_planets = []
for planet in st.session_state.planets:
    planet["y"] += planet_speed
    px, py, ps = planet["x"], planet["y"], planet["size"]

    # 우주선 충돌 체크
    if (abs(px - st.session_state.spaceship_x) < ps and
        abs(py - st.session_state.spaceship_y) < ps):
        st.session_state.game_over = True

    # 총알 충돌 체크
    hit = False
    for bullet in st.session_state.bullets:
        if abs(bullet["x"] - px) < ps and abs(bullet["y"] - py) < ps:
            hit = True
            st.session_state.score += 1
            break

    if not hit and py < canvas_height:
        new_planets.append(planet)
st.session_state.planets = new_planets

# 게임 오버 처리
if st.session_state.game_over:
    st.error("💥 게임 오버! 점수: {}".format(st.session_state.score))
    if st.button("다시 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    st.stop()

# 게임 화면 그리기
from streamlit.components.v1 import html

html_code = f"""
<canvas id="gameCanvas" width="{canvas_width}" height="{canvas_height}" 
style="border:1px solid #000;"></canvas>
<script>
var canvas = document.getElementById("gameCanvas");
var ctx = canvas.getContext("2d");

// 배경
ctx.fillStyle = "black";
ctx.fillRect(0, 0, canvas.width, canvas.height);

// 우주선
ctx.fillStyle = "white";
ctx.fillRect({st.session_state.spaceship_x}, {st.session_state.spaceship_y}, 30, 30);

// 총알
ctx.fillStyle = "yellow";
{"".join([f'ctx.fillRect({b["x"]}, {b["y"]}, 5, 10);' for b in st.session_state.bullets])}

// 행성
ctx.fillStyle = "red";
{"".join([f'ctx.beginPath();ctx.arc({p["x"]}, {p["y"]}, {p["size"]//2}, 0, 2 * Math.PI);ctx.fill();' for p in st.session_state.planets])}
</script>
"""

html(html_code)

# 점수 출력
st.markdown(f"**점수: {st.session_state.score}**")
