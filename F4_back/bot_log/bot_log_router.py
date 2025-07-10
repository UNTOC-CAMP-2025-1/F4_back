from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from pydantic import ValidationError
from bot_log.bot_log_schema import BotLogCreate
from user.auth import get_current_user_id
from models import Game_session, AI_bot, BotLog
from functools import partial
from database import get_db
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()
get_bot_log_db = partial(get_db, domain="bot_log")

@router.post("/log")
def log_batch_data(
    raw_logs: List[dict] = Body(...),  # 프론트에서 주는 로그 배열
    authorization: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_bot_log_db)
):
    user_id = get_current_user_id(authorization)

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
            log = BotLogCreate(**raw)  # 타입 검사
            valid_logs.append(log)
        except ValidationError as e:
            print(f"[SKIPPED] {i}번째 로그 형식이 올바르지 않아 저장하지 않음: {e}")

    log_ids = []
    for bot in bots:
        for log in valid_logs:
            new_log = BotLog(
                bot_id=bot.bot_id,
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
            db.flush()  # ID 미리 얻기
            log_ids.append(new_log.id)

    db.commit()

    return {
        "message": f"{len(log_ids)}개의 로그가 봇들에 대해 저장되었습니다.",
        "log_ids": log_ids
    }
