from sqlalchemy.orm import Session
from models import Character
from models import Bot_character
from fastapi import HTTPException
import random

def assign_random_bot_character(db: Session, bot_id: int):
    all_chars = db.query(Character).all()
    if not all_chars:
        raise HTTPException(status_code=404, detail="No characters available to assign")
    chosen_char = random.choice(all_chars)

    existing = db.query(Bot_character).filter_by(bot_id=bot_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Character already assigned to this bot")

    new_bot_char = Bot_character(bot_id=bot_id, character_id=chosen_char.character_id)
    db.add(new_bot_char)
    db.commit()
    db.refresh(new_bot_char)
    return new_bot_char

def delete_bot_character(db: Session, bot_id: int, character_id: int):
    bot_char = db.query(Bot_character).filter_by(bot_id=bot_id, character_id=character_id).first()
    if not bot_char:
        raise HTTPException(status_code=404, detail="Character not found")
    db.delete(bot_char)
    db.commit()

def get_bot_characters(db: Session, bot_id: int):
    return db.query(Bot_character).filter_by(bot_id=bot_id).all()

def update_bot_character(db: Session, bot_id: int, new_character_id: int):
    bot_char = db.query(Bot_character).filter_by(bot_id=bot_id).first()
    if not bot_char:
        raise HTTPException(status_code=404, detail="Bot character not found")

    bot_char.character_id = new_character_id
    db.commit()
    db.refresh(bot_char)
    return bot_char