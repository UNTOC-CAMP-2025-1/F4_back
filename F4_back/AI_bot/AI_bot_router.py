from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from AI_bot.AI_bot_schema import StateInput, ActionOutput, AIBotResponse, AIBotCreate
from AI_bot.AI_bot_crud import decide_ai_action, create_ai_bot
from AI_bot.util import get_db_by_domain
from user.auth import get_current_user_id
from database import get_db
from functools import partial
import os

router = APIRouter(prefix="/ai", tags=["AI"])
get_ai_bot_db = partial(get_db, domain="ai_bot")

@router.post("/infer", response_model=ActionOutput)
def infer_direction(
    state: StateInput,
    db: Session = Depends(get_db_by_domain("bot_log")) 
):
    action = decide_ai_action(state)
    return ActionOutput(action=action)

@router.post("/create_ai", response_model=AIBotResponse)
def create_ai_bot_endpoint(
    bot_data: AIBotCreate,
    db: Session = Depends(get_db_by_domain("AI_bot")),
    user_id: int = Depends(get_current_user_id),
):
    bot = create_ai_bot(db, bot_data, user_id=user_id)
    return bot

@router.post("/upload_weights")
async def upload_weights(file: UploadFile = File(...)):
    save_path = "./AI/weights/dqn_weights.npz"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"message": "모델 가중치 업로드 완료"}