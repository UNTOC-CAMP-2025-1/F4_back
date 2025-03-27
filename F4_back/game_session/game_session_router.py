from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from user.auth import get_user_id_from_token
from .game_session_schema import GameSessionCreate, GameSessionResponse
from .game_session_crud import (
    create_game_session, get_game_sessions_by_user, get_game_session
)

router = APIRouter()

@router.post("/", response_model=GameSessionResponse)
def create_session(
    session_data: GameSessionCreate,
    Authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    user_id = get_user_id_from_token(Authorization)
    return create_game_session(db, user_id, session_data)

@router.get("/my", response_model=list[GameSessionResponse])
def list_my_sessions(
    Authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    user_id = get_user_id_from_token(Authorization)
    return get_game_sessions_by_user(db, user_id)

@router.get("/{session_id}", response_model=GameSessionResponse)
def read_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    session = get_game_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
    return session