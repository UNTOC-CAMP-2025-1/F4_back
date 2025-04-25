from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from models import Base  # 모델을 정의한 파일에서 Base 임포트

# .env 파일에서 환경 변수를 불러옴
load_dotenv()

DB_HOST = os.environ.get("DB_HOST")  # 예: localhost
DB_PASSWORD = os.environ.get("DB_PASSWORD")  # MySQL 비밀번호
USER_DB_NAME = os.environ.get("USER_DB_NAME")  # DB 이름
DB_PORT = os.environ.get("DB_PORT", 3306)  # 기본 포트 3306

# MySQL 연결 URL 생성
DATABASE_URL = f"mysql+pymysql://root:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{USER_DB_NAME}"

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    echo=True,  # 쿼리 로그 출력
    pool_pre_ping=True,  # 연결 상태 확인
)

# 세션 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 테이블 생성
Base.metadata.create_all(bind=engine)  # 모델을 통해 테이블 자동 생성

# DB 세션을 가져오는 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()