from AI.loader import predict_direction
from AI_bot.AI_bot_schema import StateInput, AIBotCreate
from models import AI_bot
from sqlalchemy.orm import Session

def decide_ai_action(state: StateInput) -> int:
    return predict_direction(
        state.state_x, state.state_y,
        state.player_x, state.player_y
    )

def create_ai_bot(db: Session, bot_data: AIBotCreate):
    bot = AI_bot(
        session_id=bot_data.session_id,
        bot_name=bot_data.bot_name,
        bot_score=0,
        strategy_id=bot_data.strategy_id
    )
    db.add(bot)
    db.commit()
    db.refresh(bot)
    return bot