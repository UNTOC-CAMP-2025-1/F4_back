from pydantic import BaseModel

class UserCharacterCreate(BaseModel):
    character_id: int

class UserCharacterResponse(BaseModel):
    user_id: int
    character_id: int
    is_active: bool

    class Config:
        orm_mode = True