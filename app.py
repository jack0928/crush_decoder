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
        을 각각 한 문단씩 설명해줘.

        그리고 마지막에 이 상황에 어울리는 답장 한 문장을 추천해줘.
        예를 들어 “그랬구나~ 요즘 많이 바빴겠다!” 처럼 자연스럽고 현실적인 문장이면 좋아.

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
        # AI 답장 분리 (기본 패턴: "추천 답장:" 또는 "답장:")
        reply_split = bot_msg.strip().split("답장:")
        main_analysis = reply_split[0].strip()
        ai_reply = reply_split[1].strip() if len(reply_split) > 1 else None

        # 사용자 말풍선
        st.markdown(f"<div class='user-bubble'>🙋‍♀️ <b>나:</b> {user_msg}</div>", unsafe_allow_html=True)

        # 분석 결과 말풍선
        st.markdown(f"<div class='bot-bubble'>🤖 <b>분석:</b><br>{main_analysis}</div>", unsafe_allow_html=True)

        # AI 추천 답장 강조
        if ai_reply:
            st.markdown(f"<div class='bot-bubble' style='background-color:#ffe4e1;'><b>💌 AI 추천 답장:</b> {ai_reply}</div>", unsafe_allow_html=True)

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

# -------------------------------------
# 💾 대화 내보내기 기능
# -------------------------------------
if st.session_state['chat_history']:
    chat_export_text = ""
    for user_msg, bot_msg in st.session_state['chat_history']:
        chat_export_text += f"🙋‍♀️ 나: {user_msg}\n🤖 분석: {bot_msg}\n\n"

    st.download_button(
        label="📄 대화 내보내기 (.txt)",
        data=chat_export_text,
        file_name="crush_decoder_chat.txt",
        mime="text/plain"
    )


# -------------------------------------
# 🎭 썸 상대 시뮬레이션 시작
# -------------------------------------
st.divider()
st.subheader("🎮 썸 상대와 가상 대화해보기")

if st.button("🗨️ 이 사람이랑 대화해볼래요"):
    if not st.session_state['chat_history']:
        st.warning("먼저 상대의 메시지를 입력하고 분석해 주세요.")
    else:
        # 최근 메시지들로 캐릭터 스타일 추출
        messages = [msg for msg, _ in st.session_state['chat_history']]
        character_profile = "\n".join(f"- {m}" for m in messages[-5:])  # 최근 5개 기준

        # 마지막 메시지와 분석 텍스트 추출
        last_user_msg, last_bot_msg = st.session_state['chat_history'][-1]
        reply_split = last_bot_msg.strip().split("답장:")
        analysis_text = reply_split[0].strip()
        ai_reply = reply_split[1].strip() if len(reply_split) > 1 else ""

        # 캐릭터 설정 프롬프트
        st.session_state['sim_prompt'] = f"""
        너는 다음과 같은 메시지를 보낸 사람처럼 행동해야 해:

        {character_profile}

        이 사람은 썸 타는 중이며, 직설적이기보단 은근하게 감정을 표현하는 스타일이야.
        메시지를 보면 감정을 직접적으로 말하진 않지만, 약간의 거리감과 밀당이 느껴져.
        지금부터 사용자가 너에게 말을 걸면, 이 사람처럼 자연스럽게 반응해줘.

        다음은 네가 이전에 보냈던 마지막 메시지야:
        "{last_user_msg}"

        그리고 지금 너의 감정 상태는 다음과 같아:
        {analysis_text.replace('\n', ' ')} 

        그 상황을 기억하면서 대답해줘.
        말투는 자연스럽고 감정이 담긴 말투여야 해.
        """

        # 시뮬레이션 상태 초기화
        st.session_state['sim_mode'] = True
        st.session_state['sim_history'] = []

        # 첫 대사: 상대가 마지막으로 한 말을 다시 언급
        st.session_state['sim_history'].append((
            "assistant",
            last_user_msg
        ))

# -------------------------------------
# 💬 시뮬레이션 챗 인터페이스
# -------------------------------------
if st.session_state.get('sim_mode'):
    st.divider()
    st.subheader("💞 가상 썸 상대와 대화 중...")

    if 'sim_history' not in st.session_state:
        st.session_state['sim_history'] = []

    for role, msg in st.session_state['sim_history']:
        with st.chat_message(role):
            st.write(msg)

    user_msg = st.chat_input("메시지를 입력해보세요 💌")
    if user_msg:
        with st.chat_message("user"):
            st.write(user_msg)
        with st.spinner("생각 중..."):
            sim_prompt = st.session_state['sim_prompt'] + f'\n\n사용자: "{user_msg}"\n상대방:'
            reply = model.generate_content(sim_prompt).text
        st.session_state['sim_history'].append(("user", user_msg))
        st.session_state['sim_history'].append(("assistant", reply))
        with st.chat_message("assistant"):
            st.write(reply)
