from sqlalchemy.orm import Session
from models import User_character
from fastapi import HTTPException

def add_user_character_by_system(db: Session, user_id: int, character_id: int):
    db_user_char = db.query(User_character).filter_by(user_id=user_id, character_id=character_id).first()
    if db_user_char:
        return db_user_char  # 이미 보유 중이면 중복 지급 방지

    new_user_char = User_character(user_id=user_id, character_id=character_id, is_active=False)
    db.add(new_user_char)
    db.commit()
    db.refresh(new_user_char)
    return new_user_char

def delete_user_character(db: Session, user_id: int, character_id: int):
    user_char = db.query(User_character).filter_by(user_id=user_id, character_id=character_id).first()
    if not user_char:
        raise HTTPException(status_code=404, detail="Character not found")
    db.delete(user_char)
    db.commit()

def activate_user_character(db: Session, user_id: int, character_id: int):
    all_chars = db.query(User_character).filter_by(user_id=user_id).all()
    found = False
    for char in all_chars:
        char.is_active = (char.character_id == character_id)
        if char.is_active:
            found = True
    if not found:
        raise HTTPException(status_code=404, detail="Character to activate not found")
    db.commit()

def get_user_characters(db: Session, user_id: int):
    return db.query(User_character).filter_by(user_id=user_id).all()