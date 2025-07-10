from pydantic import BaseModel

class BotLogCreate(BaseModel):
    bot_number: int
    step: int
    state_x: float
    state_y: float
    player_x: float
    player_y: float
    action: int
    boost: bool
    reward: float
    event: str