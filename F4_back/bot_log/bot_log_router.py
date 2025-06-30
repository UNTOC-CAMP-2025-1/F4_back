from fastapi import APIRouter
from bot_log.bot_log_schema import BotFullState, BotAction
from bot_log.bot_log_crud import decide_action_from_strategy

router = APIRouter()

@router.post("/decide", response_model=BotAction)
def decide_action(state: BotFullState):
    result = decide_action_from_strategy(state)
    if isinstance(result, dict):
        return BotAction(**result)
    return BotAction(action=result)
