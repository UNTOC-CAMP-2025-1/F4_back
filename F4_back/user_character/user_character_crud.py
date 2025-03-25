from sqlalchemy.orm import Session
from models import User_character

def get_user_characters(db: Session, user_id: int):
    return db.query(User_character).filter(User_character.user_id == user_id).all()

def get_active_character(db: Session, user_id: int):
    return db.query(User_character).filter(
        User_character.user_id == user_id,
        User_character.is_active == True
    ).first()

def create_user_character(db: Session, user_id: int, character_id: int):
    uc = User_character(user_id=user_id, character_id=character_id, is_active=False)
    db.add(uc)
    db.commit()
    db.refresh(uc)
    return uc

def set_active_character(db: Session, user_id: int, character_id: int):
    db.query(User_character).filter(
        User_character.user_id == user_id
    ).update({"is_active": False})

    db.query(User_character).filter(
        User_character.user_id == user_id,
        User_character.character_id == character_id
    ).update({"is_active": True})

    db.commit()