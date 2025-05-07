from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from .game_session_schema import GameSessionCreate, GameSessionResponse
from .game_session_crud import (
    create_game_session, get_game_session_by_user, get_game_session_by_session
)
from user.auth import get_current_user_id

security = HTTPBearer()

router = APIRouter()

# 게임 세션 생성
@router.post("/", response_model=GameSessionResponse)
def create_session(
    session_data: GameSessionCreate,
    authorization: str = Depends(security),
    db: Session = Depends(get_db)
):
    token = authorization  # 직접 토큰을 str로 받음
    user_id = get_current_user_id(token)  # JWT 토큰에서 유저 ID 추출
    new_game_session = create_game_session(db, user_id, session_data)  # 게임 세션 생성
    return new_game_session

# 내 게임 세션 목록 조회
@router.get("/my", response_model=list[GameSessionResponse])
async def list_my_sessions(
    authorization: str = Depends(security),  # HTTPAuthorizationCredentials 대신 str로 받음
    db: Session = Depends(get_db)
):
    token = authorization  # 직접 토큰을 str로 받음
    user_id = get_current_user_id(token)  # JWT 토큰에서 유저 ID 추출
    game_sessions = get_game_session_by_user(db, user_id)  # 유저 ID로 게임 세션 조회
    return game_sessions  # 유저의 게임 세션 목록 반환

# 세션 ID로 게임 세션 조회
@router.get("/{session_id}", response_model=GameSessionResponse)
def read_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    session = get_game_session_by_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
    return session
