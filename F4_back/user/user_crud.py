from sqlalchemy.orm import Session
from models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_name(db: Session, user_name: str):
    return db.query(User).filter(User.user_name == user_name).first()

def get_user_by_email(db: Session, user_email: str):
    return db.query(User).filter(User.user_email == user_email).first()

def create_user(db: Session, user_name: str, user_email: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = User(user_name=user_name, user_email=user_email, password_hash=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def change_user_password(db: Session, user_id: int, new_password: str):
    user = db.query(User).filter(User.user_id == user_id).first()
    user.password_hash = pwd_context.hash(new_password)
    db.commit()
    db.refresh(user)
    return user

def get_user_coin(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    return user.coin if user else None

def add_user_coin(db: Session, user_id: int, amount: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        user.coin += amount
        db.commit()
        db.refresh(user)
    return user

def subtract_user_coin(db: Session, user_id: int, amount: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        if user.coin < amount:
            raise ValueError("코인이 부족합니다.")
        user.coin -= amount
        db.commit()
        db.refresh(user)
    return user