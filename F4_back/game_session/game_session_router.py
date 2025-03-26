from fastapi import APIRouter
from .game_session_schema import GameSessionCreate, GameSessionUpdate, GameSessionResponse
from typing import List

router = APIRouter(
  prefix="/game_session"
)

# 샘플 데이터 (실제로는 데이터베이스에서 가져오고 변경사항 반영하기)
game_sessions = [
    {"user_id": 1, "user_score": 500,"session_id": 1, "session_started_at": "2025-03-24T10:00:00", "session_ended_at": "2025-03-24T10:30:00"},
    {"user_id": 2, "user_score": 1000,"session_id": 2, "session_started_at": "2025-03-24T11:00:00", "session_ended_at": "2025-03-24T11:30:00"}
    # 더 많은 세션을 추가 가능
]

# / 루트 경로
# API가 제대로 작동하는지 확인하는 기본 경로
# /game_session/ 경로에 접근하면 메세지 반환환
@router.get("/")
def root():
  return {"message": "Hello from Game Session Router"}

# /get_session 경로
# game_sessions 목록에서 skip과 limit를 이용하여 게임 세션 목록 조회
# skip: 조회 시작 지점, limit: 한 번에 가져올 세션의 개수 
@router.get("/get_sessions", response_model=List[GameSessionResponse])
def get_sessions(skip: int=0, limit: int=10): # 기본값 설정해놓음음
  return game_sessions[skip: skip + limit]

# /get_sessions/{session_id} 경로
# session_id를 경로 매개변수로 받아서 해당 ID를 가진 세션 조회
# game_sessions 목록을 순차적으로 확인하여 session_id가 일치하는 세션을 찾고 반환
# 세션을 찾을 수 없다면 {"error": "Session not found"}라는 오류 메세지 반환
@router.get("/get_session/{session_id}", response_model=GameSessionResponse)
def get_session(session_id: int):
  for session in game_sessions:
    if session["session_id"] == session_id:
      return session
  return {"error": "Session not found"}
  
# 새로운 게임 세션 생성
# session_id는 자동으로 증가되도록 len(game_sessions)+1로 설정, 나머지는 요청에 따름
# 새로운 세션을 game_sesisons 목록에 추가한 후, 생성된 세션 정보 반환
@router.post("/create_session", response_model=GameSessionResponse)
def create_session(session: GameSessionCreate):
  new_session = {
    "user_id" : session.user_id,
    "user_score": session.user_score,
    "session_id": len(game_sessions) + 1,
    "session_started_at": session.session_started_at,
    "session_ended_at": session.session_ended_at
  }
  game_sessions.append(new_session)
  return new_session
  
# 게임 세션 업데이트 
# GameSessionUpdate 모델을 Python 딕셔너리로 변환하여 기존 세션에 업데이트
@router.put("/update_session/{session_id}", response_model=GameSessionResponse)
def update_session(session_id: int, session: GameSessionUpdate):
  for idx, existing_session in enumerate(game_sessions):
    if existing_session["session_id"] == session_id:
      # Pydantic 모델을 model_dump()로 딕셔너리로 변환하여 업데이트트
      game_sessions[idx].update(session.model_dump()) 
      return game_sessions[idx]
    return {"error": "Session not found"}
  
# 게임 세션 삭제
# session_id에 해당하는 게임 세션을 game_sessions 리스트에서 삭제
@router.delete("/delete_session/{session_id}")
def delete_session(session_id: int):
  for idx, session in enumerate(game_sessions):
    if session["session_id"] == session_id:
      del game_sessions[idx] # 세션 삭제
      return {"message": f"Session with ID {session_id} has been deleted"}
  return {"error": "Session not found"}
