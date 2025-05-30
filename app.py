import streamlit as st
from google.generativeai import configure, GenerativeModel
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load API key
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❗️API 키가 설정되지 않았습니다. `.streamlit/secrets.toml`을 확인해주세요.")
    st.stop()

# Configure Gemini API
configure(api_key=api_key)
model = GenerativeModel("gemini-2.5-flash-preview-05-20")

# Page setup
st.set_page_config(page_title="💘 Crush Decoder", layout="wide")

# Style customization
st.markdown("""
<style>
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
.stTextArea textarea {
    border-radius: 12px;
    border: 2px solid #ffc0cb;
    padding: 12px;
    background-color: #1e1e1e;
    color: #eee;
    font-size: 1em;
}
.stMarkdown {
    font-size: 1.1em;
    line-height: 1.6;
}
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
    font-size: 1.15em;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');

html, body, div, p, span, label, textarea, input, button, h1, h2, h3, h4, h5, h6 {
    font-family: 'Gowun Dodum', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'target_gender' not in st.session_state:
    st.session_state['target_gender'] = "여성"

st.title("💘 Crush Decoder")
st.markdown(
    "<div style='background-color:#fce4ec; color:#000000; padding:12px; border-radius:12px;'>"
    "💬 상대방의 메시지를 분석해 감정을 해석하고 대응법을 알려주는 연애 감정 분석 챗봇입니다."
    "</div>",
    unsafe_allow_html=True
)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["💌 감정 분석", "🎭 썸 시뮬레이션", "📁 대화 저장"])

# --- 감정 분석 탭 ---
with tab1:
    
    

    st.markdown("<h5>🙋‍ 상대방의 성별을 선택해주세요:</h5>", unsafe_allow_html=True)
    gender = st.radio("성별", ["여성", "남성"], horizontal=True)
    st.session_state['target_gender'] = gender

    st.markdown("<h5>💬 썸 메시지를 입력하세요:</h5>", unsafe_allow_html=True)
    user_input = st.text_area("예: 'ㅎㅎ 아냐~ 그냥 별일 없었어 ㅋㅋ'", label_visibility="collapsed")

    def analyze_message(message: str) -> str:
        try:
            gender_info = st.session_state.get('target_gender', '상대방')
            gender_text = f"{gender_info}의 말투와 성향을 고려해서,"
            prompt = f"""
            너는 연애 감정 분석 전문가야. 아래 메시지를 분석해서
            ① 감정 추정
            ② 상황 해석
            ③ 대응 팁
            을 각각 한 문단씩 설명해줘. 단 마크다운으로 보내지마.

            그리고 마지막에 이 상황에 어울리는 답장 한 문장을 추천해줘. 이때 형식은 `답장: 답장 내용` 이렇게 해줘.
            {gender_text} 자연스럽고 현실적인 말투로 대답해줘.

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

    if st.button("🔍 감정 분석하기"):
        if user_input.strip():
            with st.spinner("분석 중입니다..."):
                st.session_state['chat_history'].append((user_input, "분석 중..."))
                response = analyze_message(user_input)
                st.session_state['chat_history'][-1] = (user_input, response)
        else:
            st.warning("메시지를 입력해주세요.")

    def display_chat():
        for i, (user_msg, bot_msg) in enumerate(st.session_state['chat_history']):
            reply_split = bot_msg.strip().split("답장:")
            main_analysis = reply_split[0].strip()
            ai_reply = reply_split[1].strip() if len(reply_split) > 1 else None

            # 사용자 말풍선
            st.markdown(
                f"<div class='user-bubble'>🙋‍♀️ <b>상대방:</b> {user_msg}</div>",
                unsafe_allow_html=True
            )

            # 분석 결과 (줄바꿈 <br> + 고정된 스타일 적용)
            st.markdown(
                f"""<div class='bot-bubble' style='background-color:#ffc0cb; font-size:1.05em; line-height:1.7;'>
                <b>🤖 이 시대의 사랑 전문가:</b><br>{main_analysis.replace('\n', '<br>')}
                </div>""",
                unsafe_allow_html=True
            )

            # AI 추천 답장 (동일한 스타일)
            if ai_reply:
                st.markdown(
                    f"""<div class='bot-bubble' style='background-color:#ffe4e1; font-size:1.05em; line-height:1.7;'>
                    <b>💌 AI 추천 답장:</b> {ai_reply.replace('\n', '<br>')}
                    </div>""",
                    unsafe_allow_html=True
                )
            
    display_chat()

# --- 썸 시뮬레이션 탭 ---
with tab2:
    st.markdown("<h5>🎮 썸 상대와 가상 대화해보기</h5>", unsafe_allow_html=True)
    if st.button("🗨️ 이 사람이랑 대화해볼래요"):
        if not st.session_state['chat_history']:
            st.warning("먼저 상대의 메시지를 입력하고 분석해 주세요.")
        else:
            messages = [msg for msg, _ in st.session_state['chat_history']]
            character_profile = "\n".join(f"- {m}" for m in messages[-5:])
            last_user_msg, last_bot_msg = st.session_state['chat_history'][-1]
            reply_split = last_bot_msg.strip().split("답장:")
            analysis_text = reply_split[0].strip()

            gender = st.session_state.get('target_gender', '상대방')
            st.session_state['sim_prompt'] = f"""
            너는 다음과 같은 메시지를 보낸 **{gender}**처럼 행동해야 해:

            {character_profile}

            이 사람은 썸 타는 중이며, {gender}로서 감정을 은근하게 표현하는 편이야.
            감정 표현은 직접적이기보다 말투와 분위기로 전달돼.
            지금부터 사용자가 너에게 말을 걸면, 이 사람처럼 반응해줘.

            다음은 네가 이전에 보냈던 마지막 메시지야:
            "{last_user_msg}"

            그리고 지금 너의 감정 상태는 다음과 같아:
            {analysis_text.replace('\n', ' ')}

            이 내용을 기억하면서 대답해줘. 말투는 자연스럽고 감정이 담겨야 해.
            """
            st.session_state['sim_mode'] = True
            st.session_state['sim_history'] = [("assistant", last_user_msg)]

    if st.session_state.get('sim_mode'):
        st.markdown("🧠 이 대화는 상대의 메시지와 감정 분석 결과를 기반으로 구성된 시뮬레이션입니다. 분석된 상황과 감정을 기억한 상태에서 상대가 대화를 이어갑니다.", unsafe_allow_html=True)

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

# --- 대화 저장 탭 ---
with tab3:
    st.markdown("<h5>📁 대화 내보내기 (.txt)</h5>", unsafe_allow_html=True)
    if st.session_state['chat_history']:
        chat_export_text = ""
        for user_msg, bot_msg in st.session_state['chat_history']:
            chat_export_text += f"🙋‍♀️ 나: {user_msg}\n🤖 분석: {bot_msg}\n\n"

        st.download_button(
            label="📄 다운로드",
            data=chat_export_text,
            file_name="crush_decoder_chat.txt",
            mime="text/plain"
        )
    else:
        st.info("아직 분석된 대화가 없습니다.")


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');

html, body, [class*="css"] {
    font-family: 'Gowun Dodum', sans-serif;
}
</style>
""", unsafe_allow_html=True)
