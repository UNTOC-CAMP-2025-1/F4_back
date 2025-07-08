from sqlalchemy.orm import Session
from models import Game_session, BotLog
from .game_session_schema import GameSessionCreate
from fastapi import HTTPException
from datetime import datetime
import json
import os

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
    return (
        db.query(Game_session)
        .filter(Game_session.user_id == user_id)
        .order_by(Game_session.user_score.desc())
        .limit(10)
        .all()
    )

def get_game_session_by_session(db: Session, session_id: int):
    game_session = db.query(Game_session).filter(Game_session.session_id == session_id).first()
    if not game_session:
        raise HTTPException(status_code=404, detail="게임 세션을 찾을 수 없습니다.")
    return game_session

def end_game_session(session_id: int, db: Session):
    # 1. 게임 종료 시간 기록
    session = db.query(Game_session).filter(Game_session.session_id == session_id).first()
    if not session:
        return {"error": "Session not found"}
    
    session.session_ended_at = datetime.utcnow()
    db.commit()

    # 2. 해당 세션의 bot_log 불러오기
    bot_logs = db.query(BotLog).filter(BotLog.game_session_id == session_id).all()

    # 3. 딕셔너리 형태로 변환
    log_data = [{
        "step": log.step,
        "state_x": log.state_x,
        "state_y": log.state_y,
        "player_x": log.player_x,
        "player_y": log.player_y,
        "action": log.action,
        "boost": log.boost,
        "reward": log.reward,
        "event": log.event,
    } for log in bot_logs]

    # 4. JSON으로 저장 (Colab이 접근할 수 있는 경로 추천)
    save_path = f"./AI/logs/session_{session_id}.json"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        json.dump(log_data, f, indent=2)

    return {"message": "세션 종료 및 로그 저장 완료", "log_path": save_path}