from AI_bot.AI_bot_schema import AIBotCreate
from models import AI_bot, Game_session
from fastapi import HTTPException
from sqlalchemy.orm import Session
import os
import numpy as np

def create_ai_bot(db: Session, bot_data: AIBotCreate, user_id: int):
    session = (
        db.query(Game_session)
        .filter(Game_session.user_id == user_id)
        .order_by(Game_session.session_id.desc())
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="게임 세션을 찾을 수 없습니다.")
    
    new_bot = AI_bot(
        session_id=session.session_id,
        bot_number=bot_data.bot_number,
        user_id=user_id
    )
    db.add(new_bot)
    db.commit()
    db.refresh(new_bot)
    return new_bot

def get_bot_by_id(db: Session, bot_id: int):
    return db.query(AI_bot).filter(AI_bot.bot_id == bot_id).first()

def upload_weights(user_id: int, weights_data: dict):
    save_dir = f"./AI/weights/user_{user_id}"
    os.makedirs(save_dir, exist_ok=True)
    
    save_path = os.path.join(save_dir, "dqn_weights.npz")
    np.savez(save_path, **weights_data)
    
    print(f"[✅] Saved weights to {save_path}")
    return {"message": "Weights uploaded successfully", "path": save_path}