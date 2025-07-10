from AI.loader import predict_direction
from AI_bot.AI_bot_schema import StateInput, AIBotCreate
from models import AI_bot, Game_session
from fastapi import HTTPException
from sqlalchemy.orm import Session

def decide_ai_action(state: StateInput) -> int:
    return predict_direction(
        state.state_x, state.state_y,
        state.player_x, state.player_y
    )

def create_ai_bot(db: Session, bot_data: AIBotCreate, user_id: int):
    new_bot = AI_bot(
        session_id=bot_data.session_id,
        bot_number=bot_data.bot_number,
        user_id=user_id
    )
    db.add(new_bot)
    db.commit()
    db.refresh(new_bot)
    return new_bot

def get_bot_by_id(db: Session, bot_id: int):
    return db.query(AI_bot).filter(AI_bot.bot_id == bot_id).first()