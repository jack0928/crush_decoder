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
st.set_page_config(page_title="💘 썸 타는 감정 번역기", layout="wide")

# 스타일 설정
st.markdown(
    """
    <style>
    /* 버튼 스타일 */
    .stButton>button {
        background-color: #ffc0cb;
        color: #fff;
        border-radius: 12px;
        padding: 0.6em 1.2em;
        border: none;
        font-weight: bold;
        font-size: 1em;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ff9aad;
        transform: scale(1.05);
    }

    /* 텍스트 에어리어 */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #ffc0cb;
        padding: 12px;
        background-color: #1e1e1e;
        color: #eee;
        font-size: 1em;
    }

    /* 마크다운 텍스트 */
    .stMarkdown {
        font-size: 1.1em;
        line-height: 1.6;
    }

    /* 설명 카드 */
    .card {
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 8px;
    }

    .intro-card {
        background-color: #fce4ec;
        color: #333;
    }

    .role-card {
        background-color: #e3f2fd;
        color: #333;
    }

    /* 말풍선 UI 흉내 */
    .user-bubble {
        background-color: #333;
        color: white;
        padding: 10px;
        border-radius: 12px;
        margin-bottom: 5px;
        text-align: left;
    }

    .bot-bubble {
        background-color: #ffc0cb;
        color: black;
        padding: 10px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 페이지 제목
st.title("💘 Crush Decoder ")

# 설명 문구
st.markdown("<div class='card intro-card'>💬 상대방의 메시지를 분석해 감정을 해석하고 대응법을 알려주는 연애 감정 분석 챗봇입니다.</div>", unsafe_allow_html=True)


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
        st.markdown(f"<div class='user-bubble'>🙋‍♀️ <b>나:</b> {user_msg}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='bot-bubble'>🤖 <b>분석:</b><br>{bot_msg}</div>", unsafe_allow_html=True)

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
