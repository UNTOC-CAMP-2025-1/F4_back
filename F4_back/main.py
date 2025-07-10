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
from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/update-env", methods=["POST"])
def update_env():
    data = request.get_json()
    new_url = data.get("COLAB_WEBHOOK_URL")

    if not new_url:
        return {"error": "COLAB_WEBHOOK_URL 누락됨"}, 400

    # .env 파일 갱신
    lines = []
    env_path = ".env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()

    updated = False
    for i, line in enumerate(lines):
        if line.startswith("COLAB_WEBHOOK_URL="):
            lines[i] = f"COLAB_WEBHOOK_URL={new_url}\n"
            updated = True
            break

    if not updated:
        lines.append(f"COLAB_WEBHOOK_URL={new_url}\n")

    with open(env_path, "w") as f:
        f.writelines(lines)

    print(f"✅ COLAB_WEBHOOK_URL 갱신됨: {new_url}")
    return {"message": "env 갱신 완료"}, 200

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
app.include_router(AI_bot_router, prefix="/AI_bot", tags=["AIBot"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)