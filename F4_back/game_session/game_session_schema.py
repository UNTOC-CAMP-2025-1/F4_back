from pydantic import BaseModel

class GameSessionCreate(BaseModel):
    user_score: int | None = None

class GameSessionResponse(BaseModel):
    session_id: int
    user_id: int
    user_score: int | None = None

    class Config:
        orm_mode = True

class GameSessionStartResponse(BaseModel):
    session_id: int
    user_id: int