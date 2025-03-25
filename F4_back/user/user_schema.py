from pydantic import BaseModel

class UserCreate(BaseModel):
    user_name: str
    user_email: str
    password: str

class UserLogin(BaseModel):
    user_name: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    user_id: int
    user_name: str
    user_email: str

    class Config:
        orm_mode = True