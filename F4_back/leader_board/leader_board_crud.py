from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Game_session, User
from database import get_db

def get_top_users_from_game_sessions(limit: int = 3):
    user_db = next(get_db("user"))
    game_session_db = next(get_db("game_session"))

    try:
        subquery = (
            game_session_db.query(
                Game_session.user_id,
                func.max(Game_session.user_score).label("max_score")
            )
            .group_by(Game_session.user_id)
            .subquery()
        )

        results = (
            user_db.query(User.user_name, subquery.c.max_score)
            .join(subquery, subquery.c.user_id == User.user_id)
            .order_by(subquery.c.max_score.desc())
            .limit(limit)
            .all()
        )

        return results

    finally:
        user_db.close()
        game_session_db.close()