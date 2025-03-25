from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from models import User
from user.user_schema import UserCreate, UserLogin, UserResponse, TokenResponse
from user.user_crud import (
    get_user_by_name, get_user_by_email, create_user,
    verify_password, change_user_password
)
from user.auth import create_access_token, decode_access_token
from user.util import generate_auth_code, store_auth_code, verify_auth_code

router = APIRouter()

# 회원가입
@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_name(db, user.user_name):
        raise HTTPException(status_code=400, detail="이미 사용 중인 이름입니다.")
    if get_user_by_email(db, user.user_email):
        raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")
    return create_user(db, user.user_name, user.user_email, user.password)

# 로그인 (JWT 발급)
@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_name(db, user.user_name)
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 잘못되었습니다.")
    
    token = create_access_token({"sub": str(db_user.user_id)})
    return {"access_token": token, "token_type": "bearer"}

# 내 정보 조회 (JWT 기반)
@router.get("/me", response_model=UserResponse)
def get_me(Authorization: str = Header(...), db: Session = Depends(get_db)):
    token = Authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")

    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.user_id == user_id).first()
    return user

@router.post("/send-auth-code")
def send_auth_code(user_email: str):
    code = generate_auth_code()
    store_auth_code(user_email, code)
    print(f"[DEBUG] 인증 코드: {code} → {user_email} 전송됨")
    return {"message": "인증 코드가 이메일로 전송되었습니다."}

@router.post("/verify-auth-code")
def verify_email_code(user_email: str, code: str):
    if verify_auth_code(user_email, code):
        return {"message": "이메일 인증 성공!"}
    raise HTTPException(status_code=400, detail="인증 코드가 올바르지 않습니다.")

@router.post("/reset-password")
def reset_password(user_email: str, code: str, new_password: str, db: Session = Depends(get_db)):
    if not verify_auth_code(user_email, code):
        raise HTTPException(status_code=400, detail="인증 코드가 올바르지 않습니다.")

    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    return change_user_password(db, user.user_id, new_password)


@router.post("/change-password")
def change_password(old_password: str, new_password: str, Authorization: str = Header(...), db: Session = Depends(get_db)):
    token = Authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")
    
    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.user_id == user_id).first()
    if not verify_password(old_password, user.password_hash):
        raise HTTPException(status_code=401, detail="기존 비밀번호가 일치하지 않습니다.")
    
    return change_user_password(db, user_id, new_password)