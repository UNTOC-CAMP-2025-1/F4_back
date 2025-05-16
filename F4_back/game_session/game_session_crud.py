from sqlalchemy.orm import Session
from models import Game_session
from .game_session_schema import GameSessionCreate
from fastapi import HTTPException
from datetime import datetime

def create_game_session(db: Session, user_id: int, session_data: GameSessionCreate):
    session_started_at = session_data.session_started_at if isinstance(session_data.session_started_at, datetime) else datetime.fromisoformat(session_data.session_started_at)
    session_ended_at = session_data.session_ended_at if isinstance(session_data.session_ended_at, datetime) else datetime.fromisoformat(session_data.session_ended_at)

    session = Game_session(
        user_id=user_id,
        user_score=session_data.user_score,
        session_started_at=session_started_at,
        session_ended_at=session_ended_at
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_game_session_by_user(db: Session, user_id: int):
    return db.query(Game_session).filter(Game_session.user_id == user_id).all()

def get_game_session_by_session(db: Session, session_id: int):
    game_session = db.query(Game_session).filter(Game_session.session_id == session_id).first()
    if not game_session:
        raise HTTPException(status_code=404, detail="게임 세션을 찾을 수 없습니다.")
    return game_session