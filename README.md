# F4

## *🐍 TINIWORM Backend*

**TINIWORM은 slither.io 스타일의 멀티플레이어 뱀 게임으로, 사용자와 AI 봇이 함께 플레이하며 AI는 게임 결과를 바탕으로 학습합니다. 그냥 뱀이 아니라 유행에 맞추어 티니핑 캐릭터를 사용하였습니다. 이 레포지토리에는 게임의 백엔드 관련 내용이 들어 있습니다.**

<br>

### 🌟 기술 스택 <br>
Framework: FastAPI <br>
Database: MySQL (도메인별 분리된 DB 구조) <br>
ORM: SQLAlchemy <br>
인증/보안: JWT, OAuth2 with Bearer Token <br>
환경 설정: dotenv (.env) <br>
<br>
### 🔐 인증 및 보안 <br>
JWT 기반 로그인/회원가입 (/user/login, /user/signup) <br>
Bearer 토큰으로 유저 인증 및 액션 보호 <br>
이메일 인증 코드 발송 및 검증 포함 <br>
비밀번호 변경/재설정 기능 지원 <br>
<br>
### 🧠 AI 학습 및 구조 <br>
AI는 게임이 끝날 때마다 bot_log에 행동 로그를 저장함 <br>
이 로그는 Google Colab에서 주기적으로 학습 <br>
백엔드는 추론만 담당 (경량화 위해 torch 미포함) <br>
AI_bot은 /ai/infer 엔드포인트를 통해 행동 결정 <br>
<br>
### 🚀 주요 기능 <br>
사용자/캐릭터 관리 <br>
게임 세션 기록 및 점수 저장 <br>
AI 행동 로그 수집 <br>
리더보드 기록 <br>
JWT 기반 인증 및 코인 시스템 <br>
