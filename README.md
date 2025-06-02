# 💘 Crush Decoder  
_연애 감정 분석 챗봇 & 답장 시뮬레이터_

![image](https://github.com/user-attachments/assets/ca6af82c-be07-48cb-a981-bb540cabfa7d)


---

## 🏆 프로젝트 소개

> Basecampus 주최  
> **“이참에 해보자, AI로 코딩 한 줄 없이 서비스 기획부터 런칭까지” 원데이 해커톤**  
> 에서 탄생한 프로젝트입니다.

👉 **Crush Decoder**는 텍스트로 전달된 연애 감정을 분석하고,  
그에 어울리는 **AI 추천 답장**과 **가상 시뮬레이션**까지 제공하는  
**연애 감정 분석 특화 챗봇 서비스**입니다.  

> 🥉 이 프로젝트는 해커톤에서 **우수상**을 수상하였습니다! 야호! 🎉

---

## ✨ 주요 기능

| 기능 | 설명 |
|------|------|
| 💬 감정 분석 | 연애 상대의 카카오톡/문자 메시지를 입력하면, 감정 상태, 대화 의도, 상황 해석 등을 분석 |
| 💌 AI 추천 답장 | 분석 결과를 바탕으로, 상황에 맞는 감정적이고 자연스러운 답장 문장을 추천 |
| 🎭 답장 시뮬레이션 | 추천된 답장을 선택하면, AI와의 대화를 통해 가상의 반응을 시뮬레이션 |
| 📁 대화 저장 | 감정 분석 및 추천 내용을 `.txt` 파일로 저장 가능 |
| 🎨 직관적인 UI | Gowun Dodum 폰트와 감성적인 파스텔톤 디자인으로 꾸며진 사용자 친화적 인터페이스 |

---


## 🛠️ 사용 기술

- **🧠 Gemini 1.5 / 2.5 API**: 텍스트 감정 분석 및 자연어 응답 생성
- **🎨 Streamlit**: 프론트엔드 UI 구현
- **📝 Python (코드 최소화)**: 비개발자도 쉽게 유지보수 가능
- **🌸 Google Fonts / CSS 커스터마이징**: 감성 스타일링

---

## 🚀 사용 방법

### 1. 설치 및 실행
```bash
git clone https://github.com/yourname/crush-decoder.git
cd crush-decoder
python -m venv venv
source venv/bin/activate  # 또는 venv\\Scripts\\activate (Windows)
pip install -r requirements.txt
streamlit run app.py
```
### 2. API 키 설정
.streamlit/secrets.toml 파일에 Gemini API 키를 아래와 같이 저장하세요:
```toml
GEMINI_API_KEY = "your_api_key_here"
```
