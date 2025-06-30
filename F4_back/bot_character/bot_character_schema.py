from pydantic import BaseModel

class BotCharacterUpdateRequest(BaseModel):
    character_id: int

class BotCharacterResponse(BaseModel):
    bot_id: int
    character_id: int

    class Config:
        orm_mode = True