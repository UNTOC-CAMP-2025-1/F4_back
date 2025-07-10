from pydantic import BaseModel

class ActionOutput(BaseModel):
    action: int

class AIBotCreate(BaseModel):
    bot_number: int

class AIBotResponse(BaseModel):
    session_id: int
    bot_id: int
    user_id: int
    bot_number: int

    class Config:
        orm_mode = True