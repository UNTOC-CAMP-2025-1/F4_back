from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from user.auth import get_current_user_id
import user_character.user_character_crud as crud
from pydantic import BaseModel
from typing import List

router = APIRouter()

class CharacterRequest(BaseModel):
    character_id: int

@router.delete("/user_character/{character_id}", response_model=dict)
def delete_character(character_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    crud.delete_user_character(db, user_id=user_id, character_id=character_id)
    return {"message": "Character deleted"}

@router.patch("/user_character/{character_id}/activate", response_model=dict)
def activate_character(character_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    crud.activate_user_character(db, user_id=user_id, character_id=character_id)
    return {"message": "Character activated"}

@router.get("/user_character", response_model=List[dict])
def list_characters(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    chars = crud.get_user_characters(db, user_id=user_id)
    return [{"character_id": c.character_id, "is_active": c.is_active} for c in chars]

@router.post("/user_character", status_code=status.HTTP_201_CREATED)
def add_character(request: CharacterRequest, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    char = crud.add_user_character_by_system(db, user_id=user_id, character_id=request.character_id)
    return {"message": "Character added", "character_id": char.character_id}