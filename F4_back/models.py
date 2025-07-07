from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, TIMESTAMP, Float, func
from sqlalchemy.orm import relationship
from database import bases
"""
Base_user = bases["user"]
Base_game_session = bases["game_session"]
Base_ai_bot = bases["ai_bot"]
Base_bot_strategy = bases["bot_strategy"]
Base_leader_board = bases["leader_board"]
Base_character = bases["character"]
Base_user_character = bases["user_character"]
Base_bot_character = bases["bot_character"]
Base_bot_log = bases["bot_log"]"""

Base = list(bases.values())[0]
# User 모델 정의 (먼저 정의되어야 함)
class User(Base):
    __tablename__ = "user"
    __table_args__ = {'schema': 'user'}

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(100), unique=True, nullable=False)
    user_email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    coin = Column(Integer, default=0)
    profile_id = Column(Integer, nullable=True)
    profile_url = Column(String(255), nullable=True)

# Game_session 모델 정의
class Game_session(Base):
    __tablename__ = "game_session"
    __table_args__ = {'schema': 'game_session'}

    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user.user_id"), nullable=False)
    user_score = Column(Integer)
    session_started_at = Column(TIMESTAMP)
    session_ended_at = Column(TIMESTAMP)

# AI_bot 모델
class AI_bot(Base):
    __tablename__ = "AI_bot"
    __table_args__ = {'schema': 'AI_bot'}
    bot_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("game_session.game_session.session_id"), nullable=False)
    bot_name = Column(String(100))
    bot_score = Column(Integer)
    strategy_id = Column(Integer, ForeignKey("bot_strategy.bot_strategy.strategy_id"))

# Leader_board 모델
class Leader_board(Base):
    __tablename__ = "leader_board"
    __table_args__ = {'schema': 'leader_board'}
    leader_board_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user.user_id"))
    bot_id = Column(Integer, ForeignKey("AI_bot.AI_bot.bot_id"))
    session_id = Column(Integer, ForeignKey("game_session.game_session.session_id"))
    user_score = Column(Integer)
    rank = Column(Integer)
    score = Column(Integer)

# Bot_strategy 모델
class Bot_strategy(Base):
    __tablename__ = "bot_strategy"
    __table_args__ = {'schema': 'bot_strategy'}
    strategy_id = Column(Integer, primary_key=True)
    strategy_name = Column(String(100), nullable=False)
    description = Column(Text)

# Character 모델
class Character(Base):
    __tablename__ = "character"
    __table_args__ = {'schema': 'character'}
    character_id = Column(Integer, primary_key=True)
    image_url = Column(String(255))

# Bot_character 모델
class Bot_character(Base):
    __tablename__ = "bot_character"
    __table_args__ = {'schema': 'bot_character'}
    bot_id = Column(Integer, ForeignKey("AI_bot.AI_bot.bot_id"), primary_key=True)
    character_id = Column(Integer, ForeignKey("character.character.character_id"))

# User_character 모델
class User_character(Base):
    __tablename__ = "user_character"
    __table_args__ = {'schema': 'user_character'}
    user_id = Column(Integer, ForeignKey("user.user.user_id"), primary_key=True)
    character_id = Column(Integer, ForeignKey("character.character.character_id"), primary_key=True)
    is_active = Column(Boolean, default=False)

# Bot_log 모델
class BotLog(Base):
    __tablename__ = "bot_log"
    __table_args__ = {'schema': 'bot_log'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    bot_id = Column(Integer)
    game_session_id = Column(Integer)
    step = Column(Integer)
    timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    state_x = Column(Float)
    state_y = Column(Float)
    player_x = Column(Float)
    player_y = Column(Float)
    action = Column(Integer)
    boost = Column(Boolean, default=False)
    reward = Column(Float, default=0.0)
    event = Column(String(255), default="")