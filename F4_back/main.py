from fastapi import FastAPI
from user.user_router import router as user_router
from character.character_router import router as character_router
from user_character.user_character_router import router as user_character_router
from game_session.game_session_router import router as game_session_router

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(character_router, prefix="/character", tags=["Character"])
app.include_router(user_character_router, prefix="/user_character", tags=["UserCharacter"])
app.include_router(game_session_router, prefix="/game-session", tags=["GameSession"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)