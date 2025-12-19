import streamlit as st
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="최소공배수 알아보기 (개구리 점프)", layout="wide")
st.title("🐸 개구리 점프로 배우는 최소공배수 (LCM)")
st.write("초등학생을 위한 컬러풀한 개구리 점프 활동으로 최소공배수를 직관적으로 배워봅시다!")

# 입력
col1, col2, col3 = st.columns([1,1,2])
with col1:
    a = st.number_input("숫자 1 (작은 수)", min_value=1, max_value=10, value=3, step=1, key="lcm_a")
with col2:
    b = st.number_input("숫자 2 (큰 수)", min_value=1, max_value=10, value=4, step=1, key="lcm_b")
with col3:
    start = st.button("🚀 시작")

# 정렬: 빨강은 작은 수, 파랑은 큰 수 (같으면 동일)
small = min(a, b)
big = max(a, b)

# compute lcm
try:
    lcm_val = math.lcm(a, b)
except AttributeError:
    # for Python <3.9 fallback
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x
    lcm_val = a * b // gcd(a, b)

# Generate positions up to LCM (frogs stop at first meeting point -> LCM)
red_positions = list(range(small, lcm_val + 1, small))
blue_positions = list(range(big, lcm_val + 1, big))
meeting = lcm_val

# Visualization
st.subheader("🟢 개구리 점프 시각화")
st.write("윗줄: 빨강 개구리(작은 수), 아랫줄: 파랑 개구리(큰 수). 발자국을 따라 점프를 관찰해보세요!")

# prepare figure size: always show 20 pads per row
max_pad = 20
fig_w = 12

fig, ax = plt.subplots(figsize=(fig_w, 3))
ax.set_xlim(0.5, max_pad + 0.5)
ax.set_ylim(0, 2.2)
ax.axis('off')

# draw top and bottom lily pads (two rows)
for i in range(1, max_pad + 1):
    # top pad (red frog row)
    pad_top = plt.Circle((i, 1.5), 0.30, facecolor='#c6f7d3', edgecolor='#3aa36b')
    ax.add_patch(pad_top)
    # bottom pad (blue frog row)
    pad_bottom = plt.Circle((i, 0.5), 0.30, facecolor='#c6f7d3', edgecolor='#3aa36b')
    ax.add_patch(pad_bottom)
    # numbers under pads (centered between rows)
    ax.text(i, 0.05, str(i), ha='center', va='center', fontsize=9)

# ensure session state for shown jumps
if 'red_shown' not in st.session_state:
    st.session_state.red_shown = []
if 'blue_shown' not in st.session_state:
    st.session_state.blue_shown = []

# Controls: jump buttons and reset
btn_col1, btn_col2, btn_col3 = st.columns([1,1,8])
with btn_col1:
    if st.button("🔴 빨강 점프"):
        nextp = (st.session_state.red_shown[-1] if st.session_state.red_shown else 0) + small
        st.session_state.red_shown.append(nextp)
    st.write(f"빨강 점프 횟수: {len(st.session_state.red_shown)}")
with btn_col2:
    if st.button("🔵 파랑 점프"):
        nextp = (st.session_state.blue_shown[-1] if st.session_state.blue_shown else 0) + big
        st.session_state.blue_shown.append(nextp)
    st.write(f"파랑 점프 횟수: {len(st.session_state.blue_shown)}")
with btn_col3:
    if st.button("초기화"):
        st.session_state.red_shown = []
        st.session_state.blue_shown = []

# compute displayed footprints from session (persistent)
red_positions_display = [p for p in st.session_state.red_shown if 1 <= p <= max_pad]
blue_positions_display = [p for p in st.session_state.blue_shown if 1 <= p <= max_pad]

# draw footprints (persistent revealed ones)
for p in red_positions_display:
    ax.plot(p, 1.5, marker='o', markersize=14, color='#ff6b6b', markeredgecolor='darkred')
for p in blue_positions_display:
    ax.plot(p, 0.5, marker='o', markersize=14, color='#5ea8ff', markeredgecolor='#0b57c6')

# highlight overlapping pads within display (both frogs have landed here)
overlaps = sorted(set(red_positions_display) & set(blue_positions_display))
for p in overlaps:
    ax.add_patch(plt.Circle((p, 1.0), 0.45, facecolor='#fff0b3', edgecolor='#ffcc33', linewidth=2))
    # show frog emojis slightly offset
    ax.text(p - 0.18, 1.55, "🐸", fontsize=16)
    ax.text(p + 0.18, 0.45, "🐸", fontsize=16)

# if actual meeting (LCM) is within display, mark it specially
if 1 <= lcm_val <= max_pad:
    ax.add_patch(plt.Circle((lcm_val, 1.0), 0.55, facecolor='none', edgecolor='#ff0000', linewidth=2))
    ax.text(lcm_val, 1.0, "★", fontsize=18, ha='center', va='center', color='#ff0000')
else:
    # if meeting is beyond display, show note
    ax.text(max_pad + 0.4, 1.9, f"(최소공배수은 {lcm_val}이며, 표시된 20 연잎 밖에 있습니다)", fontsize=9, ha='right')

st.pyplot(fig)

st.markdown("---")

# 문제 섹션
st.subheader("❓ 문제 — 직접 답해보세요")
st.write("발자국을 보고 아래 문제에 답해보세요. 맞추면 결과를 알려줍니다!")

# Helper to parse list input
def parse_list_input(text):
    text = text.strip()
    if not text:
        return []
    try:
        parts = [int(x.strip()) for x in text.split(',') if x.strip()]
        return parts
    except:
        return None

# Problem 1
st.write("1) 빨강 개구리는 몇 번째 연잎만 밟았나요? (쉼표로 구분해서 적어보세요)")
col1, col2 = st.columns([3,1])
with col1:
    ans1 = st.text_input("빨강(예: 3,6,9)", key='lcm_q1')
with col2:
    if st.button("확인 1", key='check_q1'):
        user = parse_list_input(ans1)
        if user is None:
            st.error("입력 형식이 잘못되었습니다. 쉼표로 구분된 숫자를 입력하세요.")
        else:
            if user == red_positions:
                st.success("✅ 정답입니다! 빨강 개구리가 밟은 연잎 번호가 맞습니다.")
                st.info(f"빨강 개구리가 밟은 연잎: {red_positions}")
            else:
                st.error("❌ 틀렸습니다. 다시 확인해보세요.")
                st.warning("힌트: 각 개구리가 밟은 연잎 번호를 순서대로 확인해보세요")

# Problem 2
st.write("2) 파랑 개구리는 몇 번째 연잎만 밟았나요? (쉼표로 구분)")
col1, col2 = st.columns([3,1])
with col1:
    ans2 = st.text_input("파랑(예: 4,8,12)", key='lcm_q2')
with col2:
    if st.button("확인 2", key='check_q2'):
        user = parse_list_input(ans2)
        if user is None:
            st.error("입력 형식이 잘못되었습니다. 쉼표로 구분된 숫자를 입력하세요.")
        else:
            if user == blue_positions:
                st.success("✅ 정답입니다! 파랑 개구리가 밟은 연잎 번호가 맞습니다.")
                st.info(f"파랑 개구리가 밟은 연잎: {blue_positions}")
            else:
                st.error("❌ 틀렸습니다. 다시 확인해보세요.")
                st.warning("힌트: 각 개구리가 밟은 연잎 번호를 순서대로 확인해보세요")

# Problem 3
st.write("3) 빨강 개구리와 파랑 개구리는 몇 번째 연잎에서 만났나요? (숫자만 입력)")
col1, col2 = st.columns([3,1])
with col1:
    ans3 = st.number_input("만난 연잎 번호", min_value=1, max_value=100, value=lcm_val, key='lcm_q3')
with col2:
    if st.button("확인 3", key='check_q3'):
        if ans3 == lcm_val:
            st.success("✅ 정답입니다! 만난 연잎 번호가 최소공배수입니다.")
            st.info(f"설명: {small}의 배수(빨강) = {red_positions}\n{big}의 배수(파랑) = {blue_positions}\n공통인 첫 번호(최소공배수) = {lcm_val}")
        else:
            st.error("❌ 틀렸습니다. 다시 생각해보세요.")
            st.warning("힌트: 각 개구리가 밟은 연잎 번호를 차례대로 적어보면 공통으로 나오는 첫 번째 숫자가 있습니다.")

st.markdown("---")
st.write("💡 팁: 작은 수의 개구리는 빨강, 큰 수의 개구리는 파랑이에요. 두 개구리가 동시에 밟는 첫 연잎이 바로 ‘최소공배수(LCM)’입니다.")

# Footer: reset
if st.button("🔄 새로 하기"):
    st.experimental_rerun()
