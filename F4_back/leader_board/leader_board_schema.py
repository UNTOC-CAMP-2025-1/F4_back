from pydantic import BaseModel

class LeaderBoardEntry(BaseModel):
    user_name: str
    user_score: int

    class Config:
        orm_mode = True