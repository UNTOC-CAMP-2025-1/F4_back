from pydantic import BaseModel

class StateInput(BaseModel):
    state_x: float
    state_y: float
    player_x: float
    player_y: float

class ActionOutput(BaseModel):
    action: int