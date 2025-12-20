
import streamlit as st
from math import gcd

st.set_page_config(page_title="최대공약수 연습문제", layout="wide")
st.title("📝 최대공약수 연습문제")

# 연습문제 데이터 (문제별 (a, b) 쌍)
problems = [
	(3, 9),
	(15, 20),
	(18, 27)
]

def find_divisors(n):
	return [i for i in range(1, n+1) if n % i == 0]

if 'current_problem' not in st.session_state:
	st.session_state.current_problem = 0
if 'step' not in st.session_state:
	st.session_state.step = 1
if 'user_div1' not in st.session_state:
	st.session_state.user_div1 = ""
if 'user_div2' not in st.session_state:
	st.session_state.user_div2 = ""
if 'user_common' not in st.session_state:
	st.session_state.user_common = ""
if 'user_gcd' not in st.session_state:
	st.session_state.user_gcd = None
if 'feedback' not in st.session_state:
	st.session_state.feedback = ""

current = st.session_state.current_problem
a, b = problems[current]
div1 = find_divisors(a)
div2 = find_divisors(b)
common = sorted(list(set(div1) & set(div2)))
answer = gcd(a, b)


# 문제 번호와 안내 문구를 한 줄에, 안내 문구는 크게 두껍게
st.markdown(f"<div style='display:flex;align-items:center;gap:18px;'><span style='font-size:1.5em;font-weight:700;'>문제 {current+1}</span> <span style='font-size:1.3em;font-weight:800;color:#222;'>{a}와 {b}의 최대공약수를 단계별로 구해봅시다.</span></div>", unsafe_allow_html=True)



with st.container():
	# 문제 2(15, 20)일 때만 초록색 배경 적용
	step1_bg = "#e6ffe6" if (a, b) == (15, 20) else "#fffbe5"
	step1_border = "#66ff66" if (a, b) == (15, 20) else "#ffe066"
	st.markdown(f"<div style='background:{step1_bg};padding:18px 16px 10px 16px;border-radius:10px;border:1px solid {step1_border};margin-bottom:10px;'><b>1단계: {a}의 약수와 {b}의 약수를 각각 모두 써보세요.</b></div>", unsafe_allow_html=True)
	col1, col2 = st.columns(2)
	with col1:
		c0, c1, c2, c3 = st.columns([1,4,1,1])
		c0.markdown(f"<div style='min-width:60px;text-align:right;font-weight:600;'>{a}의 약수</div>", unsafe_allow_html=True)
		div1_input = c1.text_input(f"{a}의 약수 (예: 1,2,3)", value=st.session_state.user_div1, key=f"user_div1_input_{current}", label_visibility='collapsed')
		if 'div1_feedback' not in st.session_state:
			st.session_state.div1_feedback = ""
		if 'div1_answer' not in st.session_state:
			st.session_state.div1_answer = False
		if c2.button("확인", key="div1_check"):
			try:
				user1 = sorted([int(x.strip()) for x in div1_input.split(",") if x.strip()])
				st.session_state.user_div1 = div1_input
				st.session_state.div1_feedback = "정답입니다!" if user1 == div1 else "오답입니다. 다시 확인해보세요."
			except:
				st.session_state.div1_feedback = "입력 형식을 확인해주세요."
		if c3.button("정답", key="div1_answer_btn"):
			st.session_state.div1_answer = True
		if st.session_state.div1_feedback:
			st.info(f"{a}의 약수: {st.session_state.div1_feedback}")
		if st.session_state.div1_answer:
			st.info(f"정답: {div1}")
	with col2:
		c0, c1, c2, c3 = st.columns([1,4,1,1])
		c0.markdown(f"<div style='min-width:60px;text-align:right;font-weight:600;'>{b}의 약수</div>", unsafe_allow_html=True)
		div2_input = c1.text_input(f"{b}의 약수 (예: 1,2,3)", value=st.session_state.user_div2, key=f"user_div2_input_{current}", label_visibility='collapsed')
		if 'div2_feedback' not in st.session_state:
			st.session_state.div2_feedback = ""
		if 'div2_answer' not in st.session_state:
			st.session_state.div2_answer = False
		if c2.button("확인", key="div2_check"):
			try:
				user2 = sorted([int(x.strip()) for x in div2_input.split(",") if x.strip()])
				st.session_state.user_div2 = div2_input
				st.session_state.div2_feedback = "정답입니다!" if user2 == div2 else "오답입니다. 다시 확인해보세요."
			except:
				st.session_state.div2_feedback = "입력 형식을 확인해주세요."
		if c3.button("정답", key="div2_answer_btn"):
			st.session_state.div2_answer = True
		if st.session_state.div2_feedback:
			st.info(f"{b}의 약수: {st.session_state.div2_feedback}")
		if st.session_state.div2_answer:
			st.info(f"정답: {div2}")
	st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)


with st.container():
	step2_bg = "#e6ffe6" if (a, b) == (15, 20) else "#fffbe5"
	step2_border = "#66ff66" if (a, b) == (15, 20) else "#ffe066"
	st.markdown(f"<div style='background:{step2_bg};padding:18px 16px 10px 16px;border-radius:10px;border:1px solid {step2_border};margin-bottom:10px;'><b>2단계: {a}와 {b}의 공약수를 모두 써보세요.</b></div>", unsafe_allow_html=True)
	c1, c2, c3 = st.columns([4,1,1])
	common_input = c1.text_input("공약수 (예: 1,2,3)", value=st.session_state.user_common, key=f"user_common_input_{current}", label_visibility='collapsed')
	if 'common_feedback' not in st.session_state:
		st.session_state.common_feedback = ""
	if 'common_answer' not in st.session_state:
		st.session_state.common_answer = False
	if c2.button("확인", key="common_check"):
		try:
			user_common = sorted([int(x.strip()) for x in common_input.split(",") if x.strip()])
			st.session_state.user_common = common_input
			st.session_state.common_feedback = "정답입니다!" if user_common == common else "오답입니다. 다시 확인해보세요."
		except:
			st.session_state.common_feedback = "입력 형식을 확인해주세요."
	if c3.button("정답", key="common_answer_btn"):
		st.session_state.common_answer = True
	if st.session_state.common_feedback:
		st.info(f"공약수: {st.session_state.common_feedback}")
	if st.session_state.common_answer:
		st.info(f"정답: {common}")

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)


with st.container():
	step3_bg = "#e6ffe6" if (a, b) == (15, 20) else "#fffbe5"
	step3_border = "#66ff66" if (a, b) == (15, 20) else "#ffe066"
	st.markdown(f"<div style='background:{step3_bg};padding:18px 16px 10px 16px;border-radius:10px;border:1px solid {step3_border};margin-bottom:10px;'><b>3단계: {a}와 {b}의 최대공약수를 써보세요.</b></div>", unsafe_allow_html=True)
	c1, c2, c3 = st.columns([4,1,1])
	gcd_input = c1.number_input("최대공약수", min_value=1, max_value=max(a, b), value=st.session_state.user_gcd if st.session_state.user_gcd is not None else None, key=f"user_gcd_input_{current}", label_visibility='collapsed')
	if 'gcd_feedback' not in st.session_state:
		st.session_state.gcd_feedback = ""
	if 'gcd_answer' not in st.session_state:
		st.session_state.gcd_answer = False
	if c2.button("확인", key="gcd_check"):
		st.session_state.user_gcd = gcd_input
		if gcd_input == answer:
			st.session_state.gcd_feedback = "정답입니다!"
		else:
			st.session_state.gcd_feedback = "오답입니다. 다시 확인해보세요."
	if c3.button("정답", key="gcd_answer_btn"):
		st.session_state.gcd_answer = True
	if st.session_state.gcd_feedback:
		st.info(f"최대공약수: {st.session_state.gcd_feedback}")
	if st.session_state.gcd_answer:
		st.info(f"정답: {answer}")

# 다음 문제로 이동
if 'gcd_feedback' not in st.session_state:
	st.session_state.gcd_feedback = ""
if gcd_input == answer and st.session_state.gcd_feedback == "정답입니다!":
	if current < len(problems) - 1:
		   if st.button("다음 문제로"):
			   st.session_state.current_problem += 1
			   # 모든 입력값과 피드백 초기화 (입력 위젯은 key 변경으로 자동 초기화)
			   st.session_state.user_div1 = ""
			   st.session_state.user_div2 = ""
			   st.session_state.user_common = ""
			   st.session_state.user_gcd = None
			   st.session_state.gcd_feedback = ""
			   st.session_state.div1_feedback = ""
			   st.session_state.div2_feedback = ""
			   st.session_state.common_feedback = ""
			   st.session_state.div1_answer = False
			   st.session_state.div2_answer = False
			   st.session_state.common_answer = False
			   st.session_state.gcd_answer = False
	else:
		st.success("모든 문제를 완료했습니다! 수고하셨습니다.")
		st.balloons()
