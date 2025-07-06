from sqlalchemy.orm import Session
from models import Leader_board, User

def get_top_users(db: Session, limit: int = 3):
    return (
        db.query(User.user_name, Leader_board.user_score)
        .join(User, Leader_board.user_id == User.user_id)
        .order_by(Leader_board.user_score.desc())
        .limit(limit)
        .all()
    )