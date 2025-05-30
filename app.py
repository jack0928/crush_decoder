import streamlit as st
from google.generativeai import configure, GenerativeModel
from dotenv import load_dotenv
import os

# 환경 변수 로드 (로컬 테스트용)
load_dotenv()

# secrets.toml 또는 .env에서 API 키 불러오기
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

# API 키가 설정되었는지 확인
if not api_key:
    st.error("❗️API 키가 설정되지 않았습니다. `.streamlit/secrets.toml`을 확인해주세요.")
    st.stop()

# Gemini API 구성
configure(api_key=api_key)
model = GenerativeModel("gemini-1.5-flash")

# 페이지 설정
st.set_page_config(page_title="💘 썸 타는 감정 번역기")
st.title("💘 썸 타는 감정 번역기")
st.write("상대방의 메시지를 분석해 감정을 해석하고 대응법을 알려주는 연애 감정 분석 챗봇입니다.")
st.markdown("🧠 **현재 역할:** 연애 감정 분석 전문가로 동작 중입니다.")
st.divider()

# 세션 상태 초기화 (채팅 히스토리 저장용)
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 감정 분석 함수
def analyze_message(message: str) -> str:
    try:
        prompt = f"""
        너는 연애 감정 분석 전문가야. 아래 메시지를 분석해서
        ① 감정 추정
        ② 상황 해석
        ③ 대응 팁
        을 각각 한 문단씩 설명해줘. 공감 가고 자연스러운 말투로 대답해줘.

        "{message}"
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "API key" in str(e):
            return "❗️API 키가 설정되지 않았습니다."
        elif "network" in str(e).lower():
            return "⚠️ 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        else:
            return "⚠️ 답변 생성 중 오류가 발생했습니다. 다시 시도해주세요."

# 채팅 메시지 출력 함수
def display_chat():
    for user_msg, bot_msg in st.session_state['chat_history']:
        with st.chat_message("user"):
            st.write(user_msg)
        with st.chat_message("assistant"):
            st.write(bot_msg)

# 입력 UI
st.write("### 💬 썸 메시지를 입력하세요:")
user_input = st.text_area("예: 'ㅎㅎ 아냐~ 그냥 별일 없었어 ㅋㅋ'", label_visibility="collapsed")

if st.button("🔍 감정 분석하기"):
    if user_input.strip():
        with st.spinner("분석 중입니다..."):
            st.session_state['chat_history'].append((user_input, "분석 중..."))
            response = analyze_message(user_input)
            st.session_state['chat_history'][-1] = (user_input, response)
    else:
        st.warning("메시지를 입력해주세요.")

# 대화 내용 출력
display_chat()
