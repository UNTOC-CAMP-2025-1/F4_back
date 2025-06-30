from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from functools import partial
import bot_character.bot_character_crud as crud
from pydantic import BaseModel
from typing import List
from bot_character.bot_character_schema import BotCharacterUpdateRequest, BotCharacterResponse

router = APIRouter()

get_botcharacter_db = partial(get_db, domain="bot_character")

@router.post("/bot_character/assign/{bot_id}", response_model=dict)
def assign_character_to_bot(bot_id: int, db: Session = Depends(get_botcharacter_db)):
    bot_char = crud.assign_random_bot_character(db, bot_id)
    return {"message": "Bot character assigned", "character_id": bot_char.character_id}

@router.delete("/bot_character/{bot_id}/{character_id}", response_model=dict)
def delete_character(
    bot_id: int,
    character_id: int,
    db: Session = Depends(get_botcharacter_db)
):
    crud.delete_bot_character(db, bot_id=bot_id, character_id=character_id)
    return {"message": "Character deleted"}

@router.get("/bot_character/{bot_id}", response_model=List[dict])
def list_characters(bot_id: int, db: Session = Depends(get_botcharacter_db)):
    chars = crud.get_bot_characters(db, bot_id=bot_id)
    return [{"bot_id": c.bot_id, "character_id": c.character_id} for c in chars]

@router.patch("/bot_character/{bot_id}", response_model=BotCharacterResponse)
def update_character(bot_id: int, request: BotCharacterUpdateRequest, db: Session = Depends(get_botcharacter_db)):
    updated_char = crud.update_bot_character(db, bot_id=bot_id, new_character_id=request.character_id)
    return updated_char