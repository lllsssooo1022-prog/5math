import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle
import numpy as np

st.set_page_config(page_title="최대공약수 알아보기", layout="wide")
st.title("🍎 사과로 배우는 최대공약수")

# 세션 상태 초기화
if 'num1' not in st.session_state:
    st.session_state.num1 = 12
if 'num2' not in st.session_state:
    st.session_state.num2 = 18
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'answer1' not in st.session_state:
    st.session_state.answer1 = None
if 'answer2' not in st.session_state:
    st.session_state.answer2 = None
if 'q1_hints_shown' not in st.session_state:
    st.session_state.q1_hints_shown = 0
if 'q2_hints_shown' not in st.session_state:
    st.session_state.q2_hints_shown = 0
if 'q2_revealed' not in st.session_state:
    st.session_state.q2_revealed = False

st.write("두 개의 숫자를 입력하면 사과로 어떻게 나누어지는지 확인해보세요!")

# 숫자 입력 섹션
col1, col2, col3 = st.columns(3)
with col1:
    num1 = st.number_input("첫 번째 숫자", min_value=1, max_value=100, value=12, key="input1")
with col2:
    num2 = st.number_input("두 번째 숫자", min_value=1, max_value=100, value=18, key="input2")
with col3:
    st.write("")
    st.write("")
    if st.button("✅ 확인"):
        st.session_state.num1 = num1
        st.session_state.num2 = num2
        st.session_state.submitted = True
        # reset question-specific states when new numbers are submitted
        st.session_state.q1_hints_shown = 0
        st.session_state.q2_hints_shown = 0
        st.session_state.q2_revealed = False

if st.session_state.submitted:
    num1 = st.session_state.num1
    num2 = st.session_state.num2
    
    st.divider()
    st.subheader("사과를 똑같은 개수로 몇개씩 묶을 수 있을까요?")
    
    # 슬라이더
    min_divisor = min(num1, num2)
    divisor = st.slider(
        "나누는 묶음 수를 선택하세요",
        min_value=1,
        max_value=min_divisor,
        value=1,
        step=1
    )
    
    st.divider()
    
    # 사과 시각화 함수
    def draw_apples(total_pieces, divisor, title, max_slots=None):
        fig, ax = plt.subplots(figsize=(10, 2))
        
        # 사과 전체 그리기
        num_groups = total_pieces // divisor
        remainder = total_pieces % divisor
        
        x_pos = 0
        y_pos = 0
        apple_radius = 0.35
        spacing = 0.15
        
        # 그룹으로 나눈 사과 그리기
        for group_idx in range(num_groups):
            for piece_idx in range(divisor):
                x = x_pos + (group_idx * (divisor + 1)) * (2 * apple_radius + spacing) + piece_idx * (2 * apple_radius + spacing)
                circle = Circle((x, y_pos), apple_radius, 
                              linewidth=2, edgecolor='darkred', facecolor='#FF6B6B')
                ax.add_patch(circle)
        
        # 남은 사과 그리기 (회색)
        if remainder > 0:
            for piece_idx in range(remainder):
                x = x_pos + (num_groups * (divisor + 1)) * (2 * apple_radius + spacing) + piece_idx * (2 * apple_radius + spacing)
                circle = Circle((x, y_pos), apple_radius, 
                              linewidth=2, edgecolor='gray', facecolor='#CCCCCC')
                ax.add_patch(circle)
        
        # 그룹 구분선 그리기
        for group_idx in range(1, num_groups + 1):
            x_line = group_idx * (divisor + 1) * (2 * apple_radius + spacing) - spacing/2
            ax.axvline(x=x_line, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        
        # x축 범위를 고정: max_slots가 주어지면 그 값을 사용하여 두 그림의 크기를 같게 만듭니다.
        if max_slots is None:
            xmax = x_pos + (num_groups * (divisor + 1) + remainder) * (2 * apple_radius + spacing)
        else:
            xmax = x_pos + (max_slots) * (2 * apple_radius + spacing)
        ax.set_xlim(-0.5, xmax)
        ax.set_ylim(-0.7, 0.7)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(f"{divisor}", fontsize=14, fontweight='bold', pad=20)
        
        return fig
    
    # 두 개의 사과 시각화
    # 각 숫자에 필요한 슬롯 수 계산 (묶음+남은 칸 포함)
    def calc_slots(total_pieces, divisor):
        groups = total_pieces // divisor
        rem = total_pieces % divisor
        return groups * (divisor + 1) + rem

    slots1 = calc_slots(num1, divisor)
    slots2 = calc_slots(num2, divisor)
    max_slots = max(slots1, slots2, 1)

    col1, col2 = st.columns(2)

    with col1:
        fig1 = draw_apples(num1, divisor, "", max_slots=max_slots)
        st.pyplot(fig1)
        plt.close(fig1)
        st.write(f"<h3 style='text-align: center;'>{num1}</h3>", unsafe_allow_html=True)

    with col2:
        fig2 = draw_apples(num2, divisor, "", max_slots=max_slots)
        st.pyplot(fig2)
        plt.close(fig2)
        st.write(f"<h3 style='text-align: center;'>{num2}</h3>", unsafe_allow_html=True)
    
    st.divider()
    
    # 최대공약수 계산
    from math import gcd
    gcd_value = gcd(num1, num2)
    
    st.divider()
    st.subheader("📚 학습 문제")
    
    # 문제 1: 공약수 찾기
    st.write("**문제 1️⃣: 두 사과를 공통으로 묶을 수 있는 수는 뭔가요?**")
    st.write(f"({num1}과 {num2}를 모두 나누어떨어뜨릴 수 있는 수를 모두 찾아보세요)")
    
    # 공약수 찾기
    def find_divisors(n):
        divisors = []
        for i in range(1, n + 1):
            if n % i == 0:
                divisors.append(i)
        return divisors
    
    common_divisors = []
    divisors1 = find_divisors(num1)
    divisors2 = find_divisors(num2)
    for d in divisors1:
        if d in divisors2:
            common_divisors.append(d)
    
    col1, col2, col3, col4 = st.columns([3, 0.5, 0.5, 0.8])
    with col1:
        user_answer1 = st.text_input(
            "정답을 쉼표로 구분하여 입력하세요 (예: 1,2,4)",
            key="question1"
        )
    
    with col2:
        if st.button("확인", key="check1"):
            if user_answer1.strip():
                try:
                    user_nums = [int(x.strip()) for x in user_answer1.split(',')]
                    user_nums_sorted = sorted(user_nums)
                    if user_nums_sorted == common_divisors:
                        st.success(f"✅ 정답입니다!")
                        # reset hints on correct answer
                        st.session_state.q1_hints_shown = 0
                    else:
                        st.error(f"❌ 다시 생각해보세요.")
                        # show a progressive hint when wrong
                        st.session_state.q1_hints_shown = min(3, st.session_state.q1_hints_shown + 1)
                except:
                    st.error("❌ 입력 형식이 잘못되었습니다.")
            else:
                st.error("❌ 답을 입력해주세요.")
    
    with col3:
        if st.button("정답", key="answer1"):
            st.info(f"정답: {common_divisors}")

    with col4:
        if st.button("힌트", key="hint1"):
            st.session_state.q1_hints_shown = min(3, st.session_state.q1_hints_shown + 1)

    # 힌트 표시 (점진적으로 더 많은 정보를 제공)
    if st.session_state.q1_hints_shown >= 1:
        divs1_str = ",".join(str(x) for x in divisors1)
        st.info(f"💡 힌트 1: 먼저 각 수({num1}, {num2})의 약수를 모두 적어보세요. 예: {num1}의 약수는 {divs1_str}입니다.")
    if st.session_state.q1_hints_shown >= 2:
        divs2_str = ",".join(str(x) for x in divisors2)
        st.info(f"💡 힌트 2: {num2}의 약수는 {divs2_str}입니다. 두 목록에서 공통으로 있는 수를 골라보세요.")
    if st.session_state.q1_hints_shown >= 3:
        st.info(f"💡 힌트 3: 공통 약수 목록을 확인해보세요: {common_divisors}")
    
    st.write("")
    
    # 문제 2: 최대공약수 찾기
    st.write("**문제 2️⃣: 그럼 이 숫자 중에 가장 큰 숫자가 무엇인가요?**")
    # '(이것이 ...의 최대공약수입니다)' 문구는 정답 확인 후 맞으면 보여줍니다.
    
    col1, col2, col3, col4 = st.columns([3, 0.5, 0.5, 0.8])
    with col1:
        user_answer2 = st.number_input(
            "정답을 입력하세요",
            min_value=1,
            max_value=min_divisor,
            key="question2"
        )
    
    with col2:
        if st.button("확인", key="check2"):
            if user_answer2 == gcd_value:
                # 정답 메시지와 설명을 같은 초록 박스 안에 표시합니다.
                st.success(f"✅ 정답입니다!\n(이것이 {num1}과 {num2}의 최대공약수입니다)")
                st.session_state.q2_hints_shown = 0
                st.session_state.q2_revealed = True
            else:
                st.error(f"❌ 다시 생각해보세요.")
                st.session_state.q2_hints_shown = min(2, st.session_state.q2_hints_shown + 1)
                st.session_state.q2_revealed = False
    
    with col3:
        if st.button("정답", key="answer2"):
            st.info(f"정답: {gcd_value}")

    with col4:
        if st.button("힌트", key="hint2"):
            st.session_state.q2_hints_shown = min(2, st.session_state.q2_hints_shown + 1)

    # 힌트 표시 (문제2는 문제1과 연계되어 힌트를 제공)
    if st.session_state.q2_hints_shown >= 1:
        st.info("💡 힌트 1: 최대공약수는 두 수의 공약수 중 가장 큰 수입니다. 문제1의 공약수를 확인해보세요.")
    if st.session_state.q2_hints_shown >= 2:
        st.info(f"💡 힌트 2: 문제1의 공약수: {common_divisors} -> 이 중 가장 큰 수가 최대공약수입니다.")
