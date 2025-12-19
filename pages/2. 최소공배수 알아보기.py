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

# 문제 정답 비교용: 앞에서부터 5개만 사용
def get_first_n_positions(step, n):
    return [step * i for i in range(1, n + 1)]

red_positions_5 = get_first_n_positions(small, 5)
blue_positions_5 = get_first_n_positions(big, 5)

# Visualization
st.subheader("점프 버튼을 여러 번 눌러보며 개구리가 몇 칸씩 점프하는지 확인해보세요!")

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
col1, col2, col3, col4 = st.columns([3, 0.7, 0.7, 1])
with col1:
    ans1 = st.text_input("(예: 1,2,3,4,5)", key='lcm_q1')
with col2:
    if st.button("확인", key='check_q1'):
        user = parse_list_input(ans1)
        if user is None:
            st.error("입력 형식이 잘못되었습니다. 쉼표로 구분된 숫자를 입력하세요.")
        else:
            if user == red_positions_5:
                st.success("✅ 정답입니다! 빨강 개구리가 밟은 연잎 번호가 맞습니다.")
                st.info(f"빨강 개구리가 밟은 연잎: {red_positions_5}")
            else:
                st.error("❌ 틀렸습니다. 다시 확인해보세요.")
                st.warning("힌트: 각 개구리가 밟은 연잎 번호를 순서대로 확인해보세요")
with col3:
    if st.button("정답", key="answer1"):
        st.info(f"정답: {red_positions_5}")
with col4:
    if st.button("힌트", key="hint1"):
        st.warning("힌트: 각 개구리가 밟은 연잎 번호를 순서대로 확인해보세요")

blue_jump = big
st.write(f"2) 파랑 개구리({blue_jump}칸씩 점프)는 몇 번째 연잎만 밟았나요? (앞에서부터 5개만, 쉼표로 구분해서 적어보세요)")
col1, col2, col3, col4 = st.columns([3, 0.7, 0.7, 1])
with col1:
    ans2 = st.text_input("(예: 1,2,3,4,5)", key='lcm_q2')
with col2:
    if st.button("확인", key='check_q2'):
        user = parse_list_input(ans2)
        if user is None:
            st.error("입력 형식이 잘못되었습니다. 쉼표로 구분된 숫자를 입력하세요.")
        else:
            if user == blue_positions_5:
                st.success("✅ 정답입니다! 파랑 개구리가 밟은 연잎 번호가 맞습니다.")
                st.info(f"파랑 개구리가 밟은 연잎: {blue_positions_5}")
            else:
                st.error("❌ 틀렸습니다. 다시 확인해보세요.")
                st.warning("힌트: 각 개구리가 밟은 연잎 번호를 순서대로 확인해보세요")
with col3:
    if st.button("정답", key="answer2"):
        st.info(f"정답: {blue_positions_5}")
with col4:
    if st.button("힌트", key="hint2"):
        st.warning("힌트: 각 개구리가 밟은 연잎 번호를 순서대로 확인해보세요")

# Problem 3
st.write("3) 빨강 개구리와 파랑 개구리는 몇 번째 연잎에서 만났나요?")
col1, col2, col3, col4 = st.columns([3, 0.7, 0.7, 1])
with col1:
    ans3 = st.number_input("", min_value=1, max_value=100, value=None, key='lcm_q3')
with col2:
    if st.button("확인", key='check_q3'):
        if ans3 == lcm_val:
            st.success("✅ 정답입니다! 만난 연잎 번호가 최소공배수입니다.")
        else:
            st.error("❌ 틀렸습니다. 다시 생각해보세요.")
            st.warning("힌트: 각 개구리가 밟은 연잎 번호를 차례대로 적어보면 공통으로 나오는 첫 번째 숫자가 있습니다.")
with col3:
    if st.button("정답", key="answer3"):
        st.info(f"정답: {lcm_val}")
with col4:
        if st.button("힌트", key="hint3"):
                st.warning("힌트: 각 개구리가 밟은 연잎 번호를 차례대로 적어보면 공통으로 나오는 첫 번째 숫자가 있습니다.")


# 큰 정리하기 버튼 (HTML/CSS)

# 큰 정리하기 버튼 (CSS 적용, st.button 사용)
st.markdown("""
<style>
.big-summary-btn {
    display: block;
    width: 100%;
    max-width: 480px;
    margin: 24px auto 12px auto;
    padding: 22px 0;
    font-size: 1.6rem;
    font-weight: bold;
    color: #fff;
    background: linear-gradient(90deg,#3399ff 60%,#66ccff 100%);
    border: none;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(51,153,255,0.12);
    cursor: pointer;
    text-align: center;
    transition: background 0.2s;
}
.big-summary-btn:hover {
    background: linear-gradient(90deg,#66ccff 60%,#3399ff 100%);
}
</style>
""", unsafe_allow_html=True)

show_summary = st.button("정리하기", key="show_summary")
if show_summary:
        lcm_list = [lcm_val * i for i in range(1, 6)]
        lcm_list_str = ", ".join(str(x) for x in lcm_list)
        st.markdown(f"""
        <div style='background:#eaf6ff;border-left:6px solid #3399ff;padding:16px 18px 14px 18px;border-radius:8px'>
            <h3 style='margin:0 0 12px 0;color:#3399ff;'>정리하기</h3>
            <ul style='margin:0 0 10px 0;padding-left:18px;'>
                <li style='margin-bottom:6px;'>
                    <span style='color:#0077cc;font-weight:bold;'>공배수</span>란 두 수 모두로 나누어 떨어지는 수입니다.
                </li>
                <li style='margin-bottom:6px;'>
                    <span style='color:#0077cc;font-weight:bold;'>최소공배수</span>란 두 수의 공배수 중 가장 작은 수입니다.
                </li>
            </ul>
            <div style='background:#fffbe6;padding:10px 12px;border-radius:6px;margin-bottom:8px;'>
                <strong>예시:</strong> <br>
                <span style='color:#d35400;font-weight:bold;'>{small}</span>와 <span style='color:#2980b9;font-weight:bold;'>{big}</span>의 공배수 → <span style='color:#16a085;'>{lcm_list_str}, ...</span><br>
                <span style='color:#0077cc;'>최소공배수</span> → <span style='color:#e74c3c;font-weight:bold;'>{lcm_val}</span>
            </div>
            <div style='font-size:15px;color:#555;'>
                <span style='background:#d6f5d6;padding:2px 8px;border-radius:4px;'>공배수: 여러 개, 최소공배수: 단 하나!</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

