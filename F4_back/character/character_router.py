from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from character.character_crud import get_all_characters
from character.character_schema import CharacterBase

router = APIRouter()

@router.get("/", response_model=list[CharacterBase])
def get_characters(db: Session = Depends(get_db)):
    return get_all_characters(db)