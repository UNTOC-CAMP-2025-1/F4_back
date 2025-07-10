from sqlalchemy.orm import Session
from models import Game_session, BotLog
from .game_session_schema import GameSessionCreate
from fastapi import HTTPException
import json, os, requests

from dotenv import load_dotenv
load_dotenv()

def update_latest_game_session_score(
    db: Session, user_id: int, session_data: GameSessionCreate
):
    session = (
        db.query(Game_session)
        .filter(Game_session.user_id == user_id)
        .order_by(Game_session.session_id.desc())
        .first()
    )
    if not session:
        raise HTTPException(404, detail="해당 유저의 세션이 없습니다.")

    session.user_score = session_data.user_score
    db.commit()
    db.refresh(session)
    return session

def get_game_session_by_user(db: Session, user_id: int):
    return (
        db.query(Game_session)
        .filter(Game_session.user_id == user_id)
        .order_by(Game_session.user_score.desc())
        .limit(10)
        .all()
    )

def get_game_session_by_session(db: Session, session_id: int):
    game_session = db.query(Game_session).filter(Game_session.session_id == session_id).first()
    if not game_session:
        raise HTTPException(status_code=404, detail="게임 세션을 찾을 수 없습니다.")
    return game_session

# ✅ 게임 종료 및 로그 저장 → Colab 학습 요청 포함
def end_game_session(session_id: int, db: Session, user_id: int):
    # 1. 세션 유효성 검사
    session = db.query(Game_session).filter(
        Game_session.session_id == session_id,
        Game_session.user_id == user_id
        ).first()
    if not session:
        return {"error": "Session not found or unauthorized"}
    
    # 2. 해당 세션의 bot_log 불러오기
    bot_logs = db.query(BotLog).filter(BotLog.session_id == session_id).all()

    # 3. 저장 디렉토리 확인 및 생성
    dir_path = "/home/yeondaaa/untocF4/F4_back/bot_logs"

    # 4. 로그 변환 및 JSON 저장
    log_data = [{
        "step": log.step,
        "state_x": log.state_x,
        "state_y": log.state_y,
        "player_x": log.player_x,
        "player_y": log.player_y,
        "action": log.action,
        "boost": log.boost,
        "reward": log.reward,
        "event": log.event,
    } for log in bot_logs]

    # 4. JSON으로 저장
    save_path = f"{dir_path}/session_{session_id}.json"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        json.dump(log_data, f, indent=2)

    # 5. Colab으로 학습 요청 전송
    notify_colab_to_train(session_id, session.user_id, log_data)

    return {"message": "세션 종료 및 로그 저장 + Colab 학습 요청 완료", 
            "log_path": save_path}

def notify_colab_to_train(session_id: int, log_data: list, user_id: int):
    webhook_url = os.getenv("COLAB_WEBHOOK_URL")
    if not webhook_url:
        print("[❌] COLAB_WEBHOOK_URL 환경변수가 설정되지 않았습니다.")
        return

    try:
        payload = {
            "session_id": session_id,
            "user_id": user_id,
            "logs": log_data  # 👈 JSON으로 변환된 로그 직접 전송
        }
        response = requests.post(webhook_url, json=payload)

        if response.status_code != 200:
            print(f"[❌] Colab 학습 요청 실패: {response.status_code} - {response.text}")
            return
        
        print(f"[✅] Colab에 학습 요청 완료: 세션 {session_id}")
        print("응답:", response.status_code, response.json())
    except Exception as e:
        print(f"[❌] Colab 학습 요청 실패: {e}")