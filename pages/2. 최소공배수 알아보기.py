import streamlit as st
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="최소공배수 알아보기 (개구리 점프)", layout="wide")
st.title("🐸 개구리 점프로 배우는 최소공배수")
st.write("빨강 개구리와 파랑 개구리가 있어요. 각 개구리가 연잎을 몇 칸씩 점프할지 설정해 보세요!")

# 입력
col1, col2, col3 = st.columns([1,1,2])
with col1:
    a = st.number_input("빨강 개구리 점프 칸 수", min_value=1, max_value=10, value=3, step=1, key="lcm_a")
with col2:
    b = st.number_input("파랑 개구리 점프 칸 수", min_value=1, max_value=10, value=4, step=1, key="lcm_b")
with col3:
    start = st.button("🚀 시작")

# 정렬: 빨강은 작은 수, 파랑은 큰 수 (같으면 동일)
small = min(a, b)
big = max(a, b)

# 시작 버튼을 누를 때까지 시각화와 문제를 표시하지 않음
if 'lcm_started' not in st.session_state:
    st.session_state.lcm_started = False
if start:
    st.session_state.lcm_started = True
    # 새로 시작하면 이전에 표시된 발자국은 초기화
    st.session_state.red_shown = []
    st.session_state.blue_shown = []

if not st.session_state.lcm_started:
    st.info("숫자 2개를 입력한 뒤 오른쪽의 '🚀 시작' 버튼을 눌러보세요")
    st.stop()

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
st.subheader("점프 버튼을 눌러보며 개구리가 몇 칸씩 점프하는지 확인해보세요!")

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
with btn_col2:
    if st.button("🔵 파랑 점프"):
        nextp = (st.session_state.blue_shown[-1] if st.session_state.blue_shown else 0) + big
        st.session_state.blue_shown.append(nextp)
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


# 두 개구리가 만나는 모든 지점(겹치는 곳): 처음 만남은 빨간색, 이후는 검정색 동그라미
overlaps = sorted(set(red_positions_display) & set(blue_positions_display))
for idx, p in enumerate(overlaps):
    color = '#ff0000' if idx == 0 else '#222222'
    ax.add_patch(plt.Circle((p, 1.0), 0.5, facecolor='none', edgecolor=color, linewidth=2))

# LCM이 표시 영역 밖인데 실제로 만났을 때만 안내 문구 표시
if lcm_val > max_pad:
    if lcm_val in overlaps:
        ax.text(max_pad + 0.4, 1.9, f"★ 두 개구리가 {lcm_val}에서 만났어요! (최소공배수)", fontsize=11, ha='right', color='#ff0000')
    else:
        ax.text(max_pad + 0.4, 1.9, f"(최소공배수는 {lcm_val}이며, 표시된 20 연잎 밖에 있습니다)", fontsize=9, ha='right')

st.pyplot(fig)

st.markdown("---")

# 문제 섹션
st.subheader("❓ 문제")


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

red_jump = small
# Problem 1
st.write(f"1) 빨강 개구리({red_jump}칸씩 점프)는 몇 번째 연잎만 밟았나요? (앞에서부터 5개만, 쉼표로 구분해서 적어보세요)")
col1, col_btn = st.columns([3,0.7])
with col1:
    ans1 = st.text_input("(예: 1,2,3,4,5)", key='lcm_q1')
with col_btn:
    btn1, btn2 = st.columns([1,0.95])
    with btn1:
        if st.button("확인", key='check_q1'):
            user = parse_list_input(ans1)
            answer = [small * i for i in range(1, 6)]
            if user is None:
                st.error("입력 형식이 잘못되었습니다. 쉼표로 구분된 숫자를 입력하세요.")
            elif len(user) != 5:
                st.error("다시 생각해보세요. 정답은 앞에서부터 5개만 써 주세요.")
            elif user == answer:
                st.success("✅ 정답입니다! 빨강 개구리가 밟은 연잎 번호가 맞습니다.")
                st.info(f"빨강 개구리가 밟은 연잎: {answer}")
            else:
                st.error("❌ 틀렸습니다. 다시 확인해보세요.")
                st.warning("힌트: 각 개구리가 밟은 연잎 번호를 순서대로 확인해보세요")
    with btn2:
        if st.button("정답", key='answer_q1'):
            st.info(f"정답: {[small * i for i in range(1, 6)]}")

blue_jump = big
# Problem 2
st.write(f"2) 파랑 개구리({blue_jump}칸씩 점프)는 몇 번째 연잎만 밟았나요? (앞에서부터 5개만, 쉼표로 구분)")
col1, col_btn = st.columns([3,0.7])
with col1:
    ans2 = st.text_input("(예: 1,2,3,4,5)", key='lcm_q2')
with col_btn:
    btn1, btn2 = st.columns([1,0.95])
    with btn1:
        if st.button("확인", key='check_q2'):
            user = parse_list_input(ans2)
            answer = [big * i for i in range(1, 6)]
            if user is None:
                st.error("입력 형식이 잘못되었습니다. 쉼표로 구분된 숫자를 입력하세요.")
            elif len(user) != 5:
                st.error("다시 생각해보세요. 정답은 앞에서부터 5개만 써 주세요.")
            elif user == answer:
                st.success("✅ 정답입니다! 파랑 개구리가 밟은 연잎 번호가 맞습니다.")
                st.info(f"파랑 개구리가 밟은 연잎: {answer}")
            else:
                st.error("❌ 틀렸습니다. 다시 확인해보세요.")
                st.warning("힌트: 각 개구리가 밟은 연잎 번호를 순서대로 확인해보세요")
    with btn2:
        if st.button("정답", key='answer_q2'):
            st.info(f"정답: {[big * i for i in range(1, 6)]}")

# Problem 3
st.write("3) 빨강 개구리와 파랑 개구리는 몇 번째 연잎에서 만났나요? (숫자만 입력)")
col1, col_btn = st.columns([3,0.7])
with col1:
    ans3 = st.text_input("(예: 1)", key='lcm_q3_input')
with col_btn:
    btn1, btn2 = st.columns([1,0.95])
    with btn1:
        if st.button("확인", key='check_q3'):
            try:
                user_val = int(ans3.strip())
            except:
                st.error("숫자만 입력해 주세요.")
                user_val = None
            if user_val is not None:
                st.session_state.show_summary = True
                if user_val == lcm_val:
                    st.success("✅ 정답입니다!")
                else:
                    st.error("❌ 틀렸습니다. 다시 생각해보세요.")
                    st.warning("힌트: 각 개구리가 밟은 연잎 번호를 차례대로 적어보면 공통으로 나오는 첫 번째 숫자가 있습니다.")
    with btn2:
        if st.button("정답", key='answer_q3'):
            st.info(f"정답: {lcm_val}")




# 마무리 정리: 문제 3번 확인 버튼을 눌렀을 때만 표시
if st.session_state.get('show_summary', False):
    def get_gcd(x, y):
        while y:
            x, y = y, x % y
        return x

    def get_common_divisors(x, y):
        return [d for d in range(1, min(x, y)+1) if x%d==0 and y%d==0]

    common_divs = get_common_divisors(a, b)
    gcd_val = get_gcd(a, b)

    st.markdown("---")
    st.markdown(
        f"""
        <div style='background-color:#ffdddd; padding: 18px; border-radius: 10px; margin-bottom: 16px;'>
        <span style='font-size:1.2em; font-weight:bold;'>정리</span><br><br>
        두 수의 공통인 <span style='color:red'><b>공배수</b></span>를 두 수의 <span style='color:red'><b>공배수</b></span>라고 합니다.<br>
        두 수의 공배수 중에서 가장 작은 수를 두 수의 <span style='color:red'><b>최소공배수</b></span>라고 합니다.<br><br>
        {a}와 {b}의 공약수는 {', '.join(str(x) for x in common_divs)}이고 {a}와 {b}의 최대공약수는 {gcd_val}입니다.
        </div>
        """,
        unsafe_allow_html=True
    )


