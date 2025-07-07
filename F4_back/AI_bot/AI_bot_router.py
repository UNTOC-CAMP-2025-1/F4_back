from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from AI_bot.AI_bot_schema import StateInput, ActionOutput
from AI_bot.AI_bot_crud import decide_ai_action
from AI_bot.util import get_db_by_domain

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/infer", response_model=ActionOutput)
def infer_direction(
    state: StateInput,
    db: Session = Depends(get_db_by_domain("bot_log")) 
):
    action = decide_ai_action(state)
    return ActionOutput(action=action)