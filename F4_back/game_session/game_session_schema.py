'''from pydantic import BaseModel
from datetime import datetime

# 세션 생성 시 사용될 Pydantic 모델. 클라이언트가 보낼 데이터 형식 정의의
class GameSessionCreate(BaseModel):
  user_id: int
  user_score: int
  session_started_at: datetime
  session_ended_at: datetime

# 세션 업데이트 시 사용될 Pydantic 모델
class GameSessionUpdate(BaseModel):
  user_score: int
  session_started_at: datetime
  session_ended_at: datetime

# 응답 시 사용할 모델. API에서 반환할 응답 모델델
class GameSessionResponse(BaseModel):
  user_id: int
  user_score: int
  session_id: int
  session_started_at: datetime
  session_ended_at: datetime
'''
from pydantic import BaseModel
from datetime import datetime

class GameSessionCreate(BaseModel):
    user_score: int | None = None
    session_started_at: datetime
    session_ended_at: datetime

class GameSessionResponse(BaseModel):
    session_id: int
    user_id: int
    user_score: int | None = None
    session_started_at: datetime
    session_ended_at: datetime

    class Config:
        orm_mode = True