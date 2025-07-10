from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import Game_session
from functools import partial
from datetime import datetime
from .game_session_schema import GameSessionCreate, GameSessionResponse, GameSessionStartResponse
from .game_session_crud import (
    get_game_session_by_user, get_game_session_by_session, update_latest_game_session_score,
    end_game_session
)
from user.auth import get_current_user_id
from functools import partial
from bot_log.bot_log_crud import get_bot_logs_by_session_id
import json
import os

security = HTTPBearer()

router = APIRouter()


get_game_session_db = partial(get_db, domain="game_session")

# 게임 세션 생성
@router.post("/", response_model=GameSessionResponse)
def post_score(
    session_data: GameSessionCreate,
    authorization: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_game_session_db)
):
    user_id = get_current_user_id(authorization)
    return update_latest_game_session_score(db, user_id, session_data)

@router.get("/my", response_model=list[GameSessionResponse])
async def list_my_sessions(
    authorization: str = Depends(security),
    db: Session = Depends(get_game_session_db)
):
    token = authorization
    user_id = get_current_user_id(token)
    return get_game_session_by_user(db, user_id)

# 세션 ID로 게임 세션 조회
@router.get("/{session_id}", response_model=GameSessionResponse)
def read_session(
    session_id: int,
    db: Session = Depends(get_game_session_db)
):
    session = get_game_session_by_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
    return session

@router.post("/start", response_model=GameSessionStartResponse)
def start_game_session(
    db: Session = Depends(get_game_session_db),
    user_id: int = Depends(get_current_user_id)
):
    new_session = Game_session(user_id=user_id, user_score=0)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return {
        "session_id": new_session.session_id,
        "user_id": user_id
    }

@router.post("/end")
def end_session(
    db: Session = Depends(get_game_session_db),
    user_id: int = Depends(get_current_user_id)
):
    # 여기서 최근 session_id 조회
    session = (
        db.query(Game_session)
        .filter(Game_session.user_id == user_id)
        .order_by(Game_session.session_id.desc())
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="최근 세션을 찾을 수 없습니다.")
    
    result = end_game_session(session.session_id, db, user_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/download_log/{session_id}")
def download_log(session_id: int):
    path = f"/home/yeondaaa/untocF4/F4_back/bot_logs/session_{session_id}.json"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="로그 파일 없음")
    return FileResponse(path, media_type='application/json', filename=f"session_{session_id}.json")

@router.get("/latest/{user_id}")
def get_latest_session(user_id: int, db: Session = Depends(get_db)):
    session = (
        db.query(Game_session)
        .filter(Game_session.user_id == user_id)
        .order_by(Game_session.created_at.desc())
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session.session_id}