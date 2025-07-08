from models import BotLog, AI_bot
from sqlalchemy.orm import Session
from bot_log.bot_log_schema import BotLogCreate

def create_bot_log(db: Session, bot_log: BotLogCreate):
    bot = db.query(AI_bot).filter(AI_bot.bot_id == bot_log.bot_id).first()
    session_id = bot.session_id if bot else None

    db_bot_log = BotLog(
        bot_id=bot_log.bot_id,
        session_id=session_id,
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
