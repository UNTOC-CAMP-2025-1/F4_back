# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

# 각 도메인별 DB 이름들
DBS = {
    "user": os.environ.get("USER_DB_NAME"),
    "character": os.environ.get("CHARACTER_DB_NAME"),
    "user_character": os.environ.get("USER_CHARACTER_DB_NAME"),
    "game_session": os.environ.get("GAME_SESSION_CHARACTER_DB_NAME"),
    "ai_bot": os.environ.get("AI_BOT_DB_NAME"),
    "bot_character": os.environ.get("BOT_CHARACTER_DB_NAME"),
    "bot_strategy": os.environ.get("BOT_STRATEGY_DB_NAME"),
    "leader_board": os.environ.get("LEADER_BOARD_DB_NAME"),
    "bot_log": os.environ.get("BOT_LOG"),
}

Base = declarative_base()
# 엔진/세션/베이스를 도메인별로 보관
engines = {}
sessions = {}


for domain, db_name in DBS.items():
    url = f"mysql+pymysql://root:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{db_name}"
    engine = create_engine(url, echo=True, pool_pre_ping=True)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    base = declarative_base()

    engines[domain] = engine
    sessions[domain] = session

bases = {domain: Base for domain in DBS}

# 도메인 이름 받아서 해당 도메인 세션을 yield하는 함수
def get_db(domain: str = "user"):
    db = sessions[domain]()
    try:
        yield db
    finally:
        db.close()