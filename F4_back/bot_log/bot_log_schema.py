from pydantic import BaseModel

class BotLogCreate(BaseModel):
    bot_id: int
    step: int
    state_x: float
    state_y: float
    player_x: float
    player_y: float
    action: int
    boost: bool = False
    reward: float = 0.0
    event: str = ""