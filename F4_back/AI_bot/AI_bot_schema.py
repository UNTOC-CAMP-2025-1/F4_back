from pydantic import BaseModel

class StateInput(BaseModel):
    state_x: float
    state_y: float
    player_x: float
    player_y: float

class ActionOutput(BaseModel):
    action: int

class AIBotCreate(BaseModel):
    session_id: int
    bot_id: int
    user_id: int

class AIBotResponse(BaseModel):
    session_id: int
    bot_id: int
    user_id: int