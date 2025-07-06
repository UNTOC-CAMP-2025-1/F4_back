from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 🔹 CORS 모듈 추가

from user.user_router import router as user_router
from character.character_router import router as character_router
from user_character.user_character_router import router as user_character_router
from game_session.game_session_router import router as game_session_router
from leader_board.leader_board_router import router as leader_board_router
from bot_character.bot_character_router import router as bot_character_router
from bot_log.bot_log_router import router as bot_log_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(character_router, prefix="/character", tags=["Character"])
app.include_router(user_character_router, prefix="/user_character", tags=["UserCharacter"])
app.include_router(game_session_router, prefix="/game_session", tags=["GameSession"])
app.include_router(leader_board_router, prefix="/leader_board", tags=["LeaderBoard"])
app.include_router(bot_character_router, prefix="/bot_character", tags=["BotCharacter"])
app.include_router(bot_log_router, prefix="/bot_log", tags=["BotLog"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)