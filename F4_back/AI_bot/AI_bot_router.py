from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from AI_bot.AI_bot_schema import StateInput, ActionOutput, AIBotResponse, AIBotCreate
from AI_bot.AI_bot_crud import decide_ai_action, create_ai_bot
from AI_bot.util import get_db_by_domain

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/infer", response_model=ActionOutput)
def infer_direction(
    state: StateInput,
    db: Session = Depends(get_db_by_domain("bot_log")) 
):
    action = decide_ai_action(state)
    return ActionOutput(action=action)

@router.post("/create_ai", response_model=AIBotResponse)
def create_bot(
    bot_data: AIBotCreate,
    db: Session = Depends(get_db_by_domain("ai_bot"))
):
    bot = create_ai_bot(db, bot_data)
    return bot