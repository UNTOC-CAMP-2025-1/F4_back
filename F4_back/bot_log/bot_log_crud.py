from models import BotLog, AI_bot, Game_session
from sqlalchemy.orm import Session
from fastapi import HTTPException
from bot_log.bot_log_schema import BotLogCreate
from pydantic import ValidationError
from typing import List

def create_bot_logs(db: Session, user_id: int, raw_logs: List[dict]):
    session = (
        db.query(Game_session)
        .filter(Game_session.user_id == user_id)
        .order_by(Game_session.session_id.desc())
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="최근 게임 세션이 없습니다.")

    bots = db.query(AI_bot).filter(AI_bot.session_id == session.session_id).all()
    if not bots:
        raise HTTPException(status_code=404, detail="해당 세션에 연결된 봇이 없습니다.")

    valid_logs = []
    for i, raw in enumerate(raw_logs):
        try:
            log = BotLogCreate(**raw)
            valid_logs.append(log)
        except ValidationError as e:
            print(f"[SKIPPED] {i}번째 로그 형식 오류: {e}")

    log_ids = []
    for log in valid_logs:
        matching_bot = next((b for b in bots if b.bot_number == log.bot_number), None)
        if not matching_bot:
            continue

        new_log = BotLog(
            bot_number=log.bot_number,
            session_id=session.session_id,
            step=log.step,
            state_x=log.state_x,
            state_y=log.state_y,
            player_x=log.player_x,
            player_y=log.player_y,
            action=log.action,
            boost=log.boost,
            reward=log.reward,
            event=log.event
        )
        db.add(new_log)
        db.flush()
        log_ids.append(new_log.id)

    db.commit()
    return {"message": f"{len(log_ids)}개의 로그 저장 완료", "log_ids": log_ids}

def get_bot_logs_by_session_id(db: Session, session_id: int):
    logs = db.query(BotLog).filter(BotLog.session_id == session_id).all()
    return logs