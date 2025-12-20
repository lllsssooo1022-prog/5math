
import streamlit as st

def lcm(a, b):
	def gcd(x, y):
		while y:
			x, y = y, x % y
		return x
	return a * b // gcd(a, b)

def multiples(n, count=10):
	return [n * i for i in range(1, count+1)]

st.title("최소공배수 구하기 연습문제")

# 단계별 문제 및 세부 단계 상태 저장
if 'problem_idx' not in st.session_state:
	st.session_state['problem_idx'] = 0
if 'substep' not in st.session_state:
	st.session_state['substep'] = 1

def next_substep():
	st.session_state['substep'] += 1

def next_problem():
	st.session_state['problem_idx'] += 1
	st.session_state['substep'] = 1

problems = [
	{"nums": (3, 5)},
	{"nums": (6, 8)},
	{"nums": (10, 15)}
]

problem_idx = st.session_state['problem_idx']
substep = st.session_state['substep']

if problem_idx >= len(problems):
	st.success("모든 문제를 완료했습니다! 수고하셨습니다.")
else:
	a, b = problems[problem_idx]["nums"]
	st.header(f"문제 {problem_idx+1}: {a}와 {b}의 최소공배수 구하기")


	# 1단계: 두 수의 배수 10개씩 쓰기 (제목 한 번만)
	color1 = '#c8e6c9' if problem_idx == 1 else '#fff9c4'
	st.markdown(f'<div style="background-color:{color1};padding:8px 12px;border-radius:6px;font-weight:bold;font-size:1.1em;display:inline-block;">1단계: {a}와 {b}의 배수 10개씩 쓰기</div>', unsafe_allow_html=True)

	user_multiples_a = st.text_input(f"{a}의 배수 10개를 ,로 구분해서 입력하세요.", key=f"mul_a_{problem_idx}")
	correct_a = multiples(a)
	col1a, col2a = st.columns([1,1])
	with col1a:
		if st.button("확인", key=f"chk1a_{problem_idx}"):
			try:
				user_list_a = [int(x.strip()) for x in user_multiples_a.split(",") if x.strip()]
				if user_list_a == correct_a:
					st.success(f"정답입니다! ({a}의 배수)")
				else:
					st.error(f"틀렸습니다. 다시 시도해보세요. ({a}의 배수)")
			except:
				st.error("입력값을 확인해주세요. 숫자와 쉼표로만 입력하세요.")
	with col2a:
		if st.button("정답", key=f"ans1a_{problem_idx}"):
			st.info(f"{a}의 배수: {correct_a}")

	user_multiples_b = st.text_input(f"{b}의 배수 10개를 ,로 구분해서 입력하세요.", key=f"mul_b_{problem_idx}")
	correct_b = multiples(b)
	col1b, col2b = st.columns([1,1])
	with col1b:
		if st.button("확인", key=f"chk1b_{problem_idx}"):
			try:
				user_list_b = [int(x.strip()) for x in user_multiples_b.split(",") if x.strip()]
				if user_list_b == correct_b:
					st.success(f"정답입니다! ({b}의 배수)")
				else:
					st.error(f"틀렸습니다. 다시 시도해보세요. ({b}의 배수)")
			except:
				st.error("입력값을 확인해주세요. 숫자와 쉼표로만 입력하세요.")
	with col2b:
		if st.button("정답", key=f"ans1b_{problem_idx}"):
			st.info(f"{b}의 배수: {correct_b}")


	# 2단계: 두 수의 공배수 쓰기
	color2 = '#c8e6c9' if problem_idx == 1 else '#fff9c4'
	st.markdown(f'<div style="background-color:{color2};padding:8px 12px;border-radius:6px;font-weight:bold;font-size:1.1em;display:inline-block;">2단계: {a}와 {b}의 공배수 쓰기</div>', unsafe_allow_html=True)
	st.markdown('<span style="font-size: 0.9em; color: #666;">(1단계에서 쓴 수 중에서 공통된 수만 골라 쓰세요)</span>', unsafe_allow_html=True)
	user_common = st.text_input("공배수를 ,로 구분해서 입력하세요.", key=f"common_{problem_idx}")
	common = sorted(list(set(multiples(a)) & set(multiples(b))))
	col2_1, col2_2 = st.columns([1,1])
	with col2_1:
		if st.button("확인", key=f"chk2_{problem_idx}"):
			try:
				user_list = [int(x.strip()) for x in user_common.split(",") if x.strip()]
				if user_list == common:
					st.success("정답입니다!")
				else:
					st.error("틀렸습니다. 다시 시도해보세요.")
			except:
				st.error("입력값을 확인해주세요. 숫자와 쉼표로만 입력하세요.")
	with col2_2:
		if st.button("정답", key=f"ans2_{problem_idx}"):
			st.info(f"공배수: {common}")


	# 3단계: 최소공배수 쓰기
	color3 = '#c8e6c9' if problem_idx == 1 else '#fff9c4'
	st.markdown(f'<div style="background-color:{color3};padding:8px 12px;border-radius:6px;font-weight:bold;font-size:1.1em;display:inline-block;">3단계: {a}와 {b}의 최소공배수 쓰기</div>', unsafe_allow_html=True)
	user_lcm = st.number_input("최소공배수를 입력하세요:", min_value=1, step=1, key=f"lcm_{problem_idx}")
	answer = lcm(a, b)
	col3_1, col3_2 = st.columns([1,1])
	with col3_1:
		if st.button("확인", key=f"chk3_{problem_idx}"):
			if user_lcm == answer:
				if problem_idx == len(problems) - 1:
					st.success("정답입니다! 모든 문제를 다 풀었습니다. 수고하셨습니다!")
					st.balloons()
				else:
					st.success("정답입니다! 다음 문제로 이동하세요.")
					st.button("다음 문제", on_click=next_problem, key=f"next3_{problem_idx}")
			else:
				st.error("틀렸습니다. 다시 시도해보세요.")
	with col3_2:
		if st.button("정답", key=f"ans3_{problem_idx}"):
			st.info(f"최소공배수: {answer}")
