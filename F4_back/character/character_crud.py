from sqlalchemy.orm import Session
from models import Character

def get_all_characters(db: Session):
    return db.query(Character).all()

def get_character_by_id(db: Session, character_id: int):
    return db.query(Character).filter(Character.character_id == character_id).first()

def create_character(db: Session, image_url: str):
    new_char = Character(
        image_url=image_url
    )
    db.add(new_char)
    db.commit()
    db.refresh(new_char)
    return new_char

def delete_character(db: Session, character_id: int):
    character = get_character_by_id(db, character_id)
    if character:
        db.delete(character)
        db.commit()
    return character