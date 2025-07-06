from sqlalchemy.orm import Session
from models import Game_session, User
from database import get_db

def get_top_users_from_game_sessions(limit: int = 3):
    user_db = next(get_db("user"))
    game_session_db = next(get_db("game_session"))

    try:
        return (
            game_session_db.query(User.user_name, Game_session.user_score)
            .join(User, Game_session.user_id == User.user_id)
            .order_by(Game_session.user_score.desc())
            .limit(limit)
            .all()
        )
    finally:
        user_db.close()
        game_session_db.close()