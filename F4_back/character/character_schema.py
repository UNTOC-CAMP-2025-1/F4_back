from pydantic import BaseModel

class CharacterBase(BaseModel):
    character_id: int
    image_url: str

    class Config:
        orm_mode = True

class CharacterCreate(BaseModel):
    image_url: str