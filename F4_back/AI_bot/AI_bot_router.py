from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from AI_bot.AI_bot_schema import AIBotResponse, AIBotCreate
from AI_bot.AI_bot_crud import create_ai_bot
from AI_bot.util import get_db_by_domain
from user.auth import get_current_user_id
from database import get_db
from functools import partial
from AI_bot.AI_bot_crud import upload_weights

router = APIRouter(prefix="/ai", tags=["AI"])
get_ai_bot_db = partial(get_db, domain="ai_bot")

@router.post("/create_ai", response_model=AIBotResponse)
def create_ai_bot_endpoint(
    bot_data: AIBotCreate,
    db: Session = Depends(get_db_by_domain("AI_bot")),
    user_id: int = Depends(get_current_user_id),
):
    bot = create_ai_bot(db, bot_data, user_id=user_id)
    return bot

security = HTTPBearer()

@router.post("/upload_weights")
def upload_ai_weights(
    weights: dict,
    user_id: int = Depends(get_current_user_id)
):
    return upload_weights(user_id, weights)