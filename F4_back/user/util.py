import random
from database import get_db
from sqlalchemy.orm import Session

email_auth_codes = {}

def generate_auth_code():
    return str(random.randint(100000, 999999))

def store_auth_code(user_email: str, code: str):
    email_auth_codes[user_email] = code

def verify_auth_code(user_email: str, code: str):
    return email_auth_codes.get(user_email) == code

def get_user_db() -> Session:
    return next(get_db("user"))

# user/util.py

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
    msg["From"] = EMAIL_USER
    msg["To"] = user_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"[DEBUG] 인증 코드 이메일 전송 성공: {user_email}")
    except Exception as e:
        print(f"[ERROR] 이메일 전송 실패: {e}")