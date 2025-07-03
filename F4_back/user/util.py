import random
from datetime import datetime, timedelta
from database import get_db
from sqlalchemy.orm import Session

# 인증 코드 저장소 (이메일, 코드, 만료 시간)
email_auth_codes = {}

# 인증 코드 생성 함수
def generate_auth_code():
    return str(random.randint(100000, 999999))

# 인증 코드 저장 함수 (만료 시간도 함께 저장)
def store_auth_code(user_email: str, code: str, expiration_time: datetime):
    expiration_time = datetime.now() + timedelta(minutes=10)  # 인증 코드 10분 후 만료
    email_auth_codes[user_email] = {'code': code, 'expiration': expiration_time}

# 인증 코드 검증 함수 (만료 시간도 확인)
def verify_auth_code(user_email: str, code: str):
    auth_info = email_auth_codes.get(user_email)
    if not auth_info:
        return False
    # 만료 시간 확인
    if auth_info['expiration'] < datetime.now():
        del email_auth_codes[user_email]  # 만료된 코드 삭제
        return False
    return auth_info['code'] == code

# 인증 코드 유효성 검사 후, 만료된 경우 새 코드 발송
def resend_auth_code(user_email: str):
    code = generate_auth_code()
    store_auth_code(user_email, code)  # 새 코드 저장
    send_email_code(user_email, code)  # 이메일로 코드 전송
    return {"message": "새 인증 코드가 이메일로 전송되었습니다."}

def get_user_db() -> Session:
    return next(get_db("user"))

# 이메일 코드 발송 함수 (변경 없음)
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email_code(user_email: str, code: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEText(f"[TINIWORM 인증]\n\n요청하신 인증 코드는 [{code}] 입니다.")
    msg["Subject"] = "인증 코드 안내"
    msg["From"] = "TINIWORM"
    msg["To"] = user_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"[DEBUG] 인증 코드 이메일 전송 성공: {user_email}")
    except Exception as e:
        print(f"[ERROR] 이메일 전송 실패: {e}")
