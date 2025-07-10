from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import Game_session
from functools import partial
from datetime import datetime
from .game_session_schema import GameSessionCreate, GameSessionResponse, GameSessionStartResponse
from .game_session_crud import (
    get_game_session_by_user, get_game_session_by_session, update_latest_game_session_score
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
    session_id: int,
    db: Session = Depends(get_game_session_db)
):
    # 1. 세션 종료 처리 (user_score는 DB에 이미 존재한다고 가정)
    session = db.query(Game_session).filter(Game_session.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="해당 세션이 존재하지 않습니다.")

    session.session_ended_at = datetime.now()
    db.commit()

    # 2. 해당 세션의 bot_log 가져오기
    bot_logs = get_bot_logs_by_session_id(db, session_id)

    # 3. 저장 디렉토리 확인 및 생성
    dir_path = "/home/yeondaaa/untocF4/F4_back/bot_logs"
    os.makedirs(dir_path, exist_ok=True)

    # 4. 파일 경로 설정 및 저장
    save_path = f"{dir_path}/session_{session_id}.json"
    with open(save_path, "w") as f:
        json.dump([log.to_dict() for log in bot_logs], f)

    return {"message": "세션 종료 및 로그 저장 완료"}