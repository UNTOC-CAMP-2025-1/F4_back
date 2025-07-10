from typing import List
from fastapi import APIRouter, Depends,  Body
from sqlalchemy.orm import Session
from user.auth import get_current_user_id
from functools import partial
from database import get_db
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bot_log.bot_log_crud import create_bot_logs

router = APIRouter()
security = HTTPBearer()
get_bot_log_db = partial(get_db, domain="bot_log")

@router.post("/log")
def log_batch_data(
    raw_logs: List[dict] = Body(...),
    authorization: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_bot_log_db)
):
    user_id = get_current_user_id(authorization)
    return create_bot_logs(db, user_id, raw_logs)
