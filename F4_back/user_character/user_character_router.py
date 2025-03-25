from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from user.auth import get_user_id_from_token
from user_character.user_character_crud import (
    get_user_characters, get_active_character,
    create_user_character, set_active_character
)
from user_character.user_character_schema import UserCharacterCreate, UserCharacterResponse

router = APIRouter()

@router.get("/my", response_model=list[UserCharacterResponse])
def get_my_characters(Authorization: str = Header(...), db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(Authorization)
    return get_user_characters(db, user_id)

@router.get("/my/active", response_model=UserCharacterResponse)
def get_active(Authorization: str = Header(...), db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(Authorization)
    active = get_active_character(db, user_id)
    if not active:
        raise HTTPException(status_code=404, detail="장착된 캐릭터가 없습니다.")
    return active

@router.post("/my/acquire", response_model=UserCharacterResponse)
def acquire_character(data: UserCharacterCreate, Authorization: str = Header(...), db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(Authorization)
    return create_user_character(db, user_id, data.character_id)

@router.patch("/my/equip/{character_id}")
def equip_character(character_id: int, Authorization: str = Header(...), db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(Authorization)
    set_active_character(db, user_id, character_id)
    return {"message": f"{character_id}번 캐릭터를 장착했습니다."}