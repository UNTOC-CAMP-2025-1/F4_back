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
        