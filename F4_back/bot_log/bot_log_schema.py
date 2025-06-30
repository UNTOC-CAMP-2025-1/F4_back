from pydantic import BaseModel
from typing import List


class Position(BaseModel):
    x: float
    y: float


class Enemy(BaseModel):
    head: Position
    body: List[Position]


class BotFullState(BaseModel):
    strategy_id: int
    bot_head: Position
    bot_body: List[Position]
    jewels: List[Position]
    corpses: List[Position]
    enemies: List[Enemy]
    bot_length: int
    can_boost: bool


class BotAction(BaseModel):
    action: int
    boost: bool = False
