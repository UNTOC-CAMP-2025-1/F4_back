from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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
def log_bot_data(
    log_data: BotLogCreate,
    authorization: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_bot_log_db)
):
    user_id = get_current_user_id(authorization)

    # 1. 가장 최근 세션 가져오기
    session = (
        db.query(Game_session)
        .filter(Game_session.user_id == user_id)
        .order_by(Game_session.session_id.desc())
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="최근 게임 세션이 없습니다.")
    
    # 2. 해당 세션에 연결된 봇 가져오기
    bots = db.query(AI_bot).filter(AI_bot.session_id == session.session_id).all()
    if not bots:
        raise HTTPException(status_code=404, detail="해당 세션에 연결된 봇이 없습니다.")

    # 3. 로그 저장
    log_ids = []
    for bot in bots:
        new_log = BotLog(
            bot_id=bot.bot_id,
            session_id=session.session_id,
            step=log_data.step,
            state_x=log_data.state_x,
            state_y=log_data.state_y,
            player_x=log_data.player_x,
            player_y=log_data.player_y,
            action=log_data.action,
            boost=log_data.boost,
            reward=log_data.reward,
            event=log_data.event
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        log_ids.append(new_log.id)

    return {
        "message": f"{len(log_ids)}개의 봇 로그 저장 완료",
        "log_ids": log_ids
    }