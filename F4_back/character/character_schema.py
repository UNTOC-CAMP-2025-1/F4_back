from pydantic import BaseModel

class CharacterBase(BaseModel):
    character_id: int
    character_name: str
    character_shape: str

    class Config:
        orm_mode = True