from sqlalchemy.orm import Session
from models import Leader_board, User
from database import get_db

def get_top_users(db: Session, limit: int = 3):
    user_db = next(get_db("user"))
    try:
        return (
            user_db.query(User.user_name, Leader_board.user_score)
            .join(Leader_board, Leader_board.user_id == User.user_id)
            .order_by(Leader_board.user_score.desc())
            .limit(limit)
            .all()
        )
    finally:
        user_db.close()