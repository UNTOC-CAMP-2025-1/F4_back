from sqlalchemy.orm import Session
from models import Game_session
from game_session_schema import GameSessionCreate

def create_game_session(db: Session, user_id: int, session_data: GameSessionCreate):
    session = Game_session(
        user_id=user_id,
        user_score=session_data.user_score,
        session_started_at=session_data.session_started_at,
        session_ended_at=session_data.session_ended_at
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_game_sessions_by_user(db: Session, user_id: int):
    return db.query(Game_session).filter(Game_session.user_id == user_id).all()

def get_game_session(db: Session, session_id: int):
    return db.query(Game_session).filter(Game_session.session_id == session_id).first()