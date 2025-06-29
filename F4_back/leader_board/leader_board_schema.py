from pydantic import BaseModel

class LeaderBoardEntry(BaseModel):
    user_id: int
    user_score: int

    class Config:
        orm_mode = True