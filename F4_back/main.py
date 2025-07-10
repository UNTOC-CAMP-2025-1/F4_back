from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 🔹 CORS 모듈 추가

from user.user_router import router as user_router
from character.character_router import router as character_router
from user_character.user_character_router import router as user_character_router
from game_session.game_session_router import router as game_session_router
from leader_board.leader_board_router import router as leader_board_router
from bot_character.bot_character_router import router as bot_character_router
from bot_log.bot_log_router import router as bot_log_router
from AI_bot.AI_bot_router import router as AI_bot_router
from fastapi import FastAPI, Request
import os

app = FastAPI()

@app.post("/update-env")
async def update_env(request: Request):
    data = await request.json()
    ngrok_url = data.get("ngrok_url")

    if not ngrok_url:
        return {"error": "ngrok_url is missing"}
    
    # .env 수정
    with open(".env", "r") as f:
        lines = f.readlines()
    with open(".env", "w") as f:
        updated = False
        for line in lines:
            if line.startswith("COLAB_WEBHOOK_URL="):
                f.write(f"COLAB_WEBHOOK_URL={ngrok_url}\n")
                updated = True
            else:
                f.write(line)
        if not updated:
            f.write(f"COLAB_WEBHOOK_URL={ngrok_url}\n")  # 없었으면 새로 추가

    # ✅ 실시간 환경변수 반영
    os.environ["COLAB_WEBHOOK_URL"] = ngrok_url

    print(f"✅ 새로운 ngrok 주소로 갱신됨: {ngrok_url}")
    return {"message": "환경변수 업데이트 완료"}

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
app.include_router(AI_bot_router, prefix="/AI_bot", tags=["AIBot"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)