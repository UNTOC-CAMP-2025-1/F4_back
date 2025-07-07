from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from bot_log.bot_log_schema import BotLogCreate
from bot_log.bot_log_crud import create_bot_log
from AI_bot.util import get_db_by_domain

router = APIRouter()

@router.post("/log")
def log_bot_data(
    log: BotLogCreate,
    db: Session = Depends(get_db_by_domain("bot_log"))
):
    return create_bot_log(db, log)