from fastapi import FastAPI
from user.user_router import router as user_router
from character.character_router import router as character_router
from user_character.user_character_router import router as user_character_router

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(character_router, prefix="/character", tags=["Character"])
app.include_router(user_character_router, prefix="/user-character", tags=["UserCharacter"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)