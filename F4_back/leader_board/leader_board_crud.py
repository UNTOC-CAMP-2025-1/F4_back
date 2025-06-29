from sqlalchemy.orm import Session
from models import Leader_board

def get_top_users(db: Session, limit: int = 3):
    return db.query(Leader_board.user_id, Leader_board.user_score)\
             .order_by(Leader_board.user_score.desc())\
             .limit(limit)\
             .all()