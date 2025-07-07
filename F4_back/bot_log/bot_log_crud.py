from models import BotLog
from sqlalchemy.orm import Session
from bot_log.bot_log_schema import BotLogCreate

def create_bot_log(db: Session, bot_log: BotLogCreate):
    db_bot_log = BotLog(
        bot_id=bot_log.bot_id,
        game_session_id=bot_log.game_session_id,
        step=bot_log.step,
        state_x=bot_log.state_x,
        state_y=bot_log.state_y,
        player_x=bot_log.player_x,
        player_y=bot_log.player_y,
        action=bot_log.action,
        boost=bot_log.boost,
        reward=bot_log.reward,
        event=bot_log.event,
    )
    db.add(db_bot_log)
    db.commit()
    db.refresh(db_bot_log)
    return db_bot_log
