from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(100), unique=True, nullable=False)
    user_email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)

    game_session = relationship("Game_session", back_populates="user")
    user_character = relationship("User_character", back_populates="user")
    leader_board = relationship("Leader_board", back_populates="user")


class Character(Base):
    __tablename__ = "character"

    character_id = Column(Integer, primary_key=True)
    character_name = Column(String(100), nullable=False)
    character_shape = Column(String(100))

    user_character = relationship("User_character", back_populates="character")
    bot_character = relationship("Bot_character", back_populates="character")


class Game_session(Base):
    __tablename__ = "game_session"

    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    user_score = Column(Integer)
    session_started_at = Column(TIMESTAMP)
    session_ended_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="game_session")
    ai_bot = relationship("AI_bot", back_populates="game_session")
    leader_board = relationship("Leader_board", back_populates="game_session")


class AI_bot(Base):
    __tablename__ = "AI_bot"

    bot_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("game_session.session_id"), nullable=False)
    bot_name = Column(String(100))
    bot_score = Column(Integer)
    strategy_id = Column(Integer, ForeignKey("bot_strategy.strategy_id"))

    game_session = relationship("Game_session", back_populates="ai_bot")
    bot_character = relationship("Bot_character", back_populates="ai_bot", uselist=False)
    bot_strategy = relationship("Bot_strategy", back_populates="ai_bot")
    leader_board = relationship("Leader_board", back_populates="ai_bot")


class Leader_board(Base):
    __tablename__ = "leader_board"

    leader_board_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    bot_id = Column(Integer, ForeignKey("AI_bot.bot_id"))
    session_id = Column(Integer, ForeignKey("game_session.session_id"))
    user_score = Column(Integer)
    rank = Column(Integer)
    score = Column(Integer)

    user = relationship("User", back_populates="leader_board")
    ai_bot = relationship("AI_bot", back_populates="leader_board")
    game_session = relationship("Game_session", back_populates="leader_board")


class User_character(Base):
    __tablename__ = "user_character"

    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    character_id = Column(Integer, ForeignKey("character.character_id"), primary_key=True)
    is_active = Column(Boolean, default=False)

    user = relationship("User", back_populates="user_character")
    character = relationship("Character", back_populates="user_character")


class Bot_character(Base):
    __tablename__ = "bot_character"

    bot_id = Column(Integer, ForeignKey("AI_bot.bot_id"), primary_key=True)
    character_id = Column(Integer, ForeignKey("character.character_id"))

    ai_bot = relationship("AI_bot", back_populates="bot_character")
    character = relationship("Character", back_populates="bot_character")


class Bot_strategy(Base):
    __tablename__ = "bot_strategy"

    strategy_id = Column(Integer, primary_key=True)
    strategy_name = Column(String(100), nullable=False)
    description = Column(Text)

    ai_bot = relationship("AI_bot", back_populates="bot_strategy")
