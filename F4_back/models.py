from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()



class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True, nullable=False)
    user_email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    game_sessions = relationship("Game_session", back_populates="user")
    user_characters = relationship("User_character", back_populates="user")
    leaderboard_entries = relationship("Leader_board", back_populates="user")


class Character(Base):
    __tablename__ = "character"

    character_id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)
    character_shape = Column(String)

    user_characters = relationship("User_character", back_populates="character")
    bot_characters = relationship("Bot_character", back_populates="character")


class Game_session(Base):
    __tablename__ = "game_session"

    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    user_score = Column(Integer)
    session_started_at = Column(TIMESTAMP)
    session_ended_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="game_sessions")
    ai_bots = relationship("AI_bot", back_populates="game_session")
    leaderboard_entries = relationship("Leader_board", back_populates="game_session")


class AI_bot(Base):
    __tablename__ = "AI_bot"

    bot_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("game_session.session_id"), nullable=False)
    bot_name = Column(String)
    bot_score = Column(Integer)
    strategy_id = Column(Integer, ForeignKey("bot_strategy.strategy_id"))

    game_session = relationship("Game_session", back_populates="AI_bots")
    bot_character = relationship("Bot_character", back_populates="bot", uselist=False)
    strategy = relationship("Bot_strategy", back_populates="bots")
    leaderboard_entries = relationship("Leader_board", back_populates="bot")


class Leader_board(Base):
    __tablename__ = "leader_board"

    leader_board_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    bot_id = Column(Integer, ForeignKey("AI_bot.bot_id"))
    session_id = Column(Integer, ForeignKey("game_session.session_id"))
    user_score = Column(Integer)
    rank = Column(Integer)
    score = Column(Integer)

    user = relationship("User", back_populates="leaderboard_entries")
    bot = relationship("AI_bot", back_populates="leaderboard_entries")
    game_session = relationship("Game_session", back_populates="leaderboard_entries")


class User_character(Base):
    __tablename__ = "user_character"

    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    character_id = Column(Integer, ForeignKey("character.character_id"), primary_key=True)
    is_active = Column(Boolean, default=False)

    user = relationship("User", back_populates="user_characters")
    character = relationship("Character", back_populates="user_characters")


class Bot_character(Base):
    __tablename__ = "bot_character"

    bot_id = Column(Integer, ForeignKey("ai_bot.bot_id"), primary_key=True)
    character_id = Column(Integer, ForeignKey("character.character_id"))

    bot = relationship("AI_bot", back_populates="bot_character")
    character = relationship("Character", back_populates="bot_characters")


class Bot_strategy(Base):
    __tablename__ = "bot_strategy"

    strategy_id = Column(Integer, primary_key=True)
    strategy_name = Column(String, nullable=False)
    description = Column(Text)

    bots = relationship("AI_bot", back_populates="strategy")