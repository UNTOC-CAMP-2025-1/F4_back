from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from character.character_crud import (
    get_all_characters, get_character_by_id,
    create_character, delete_character
)
from character.character_schema import CharacterBase, CharacterCreate

router = APIRouter()

@router.get("/", response_model=list[CharacterBase])
def get_characters(db: Session = Depends(get_db)):
    return get_all_characters(db)

# 캐릭터 생성 (관리자 기능)
@router.post("/", response_model=CharacterBase)
def add_character(character: CharacterCreate, db: Session = Depends(get_db)):
    return create_character(db, character.character_name, character.character_shape, character.image_url)

# 캐릭터 삭제 (관리자 기능)
@router.delete("/{character_id}")
def remove_character(character_id: int, db: Session = Depends(get_db)):
    character = delete_character(db, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없습니다.")
    return {"message": "삭제 완료"}

@router.get("/{character_id}", response_model=CharacterBase)
def get_character(character_id: int, db: Session = Depends(get_db)):
    character = get_character_by_id(db, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없습니다.")
    return character