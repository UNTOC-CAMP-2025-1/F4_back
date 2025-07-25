from fastapi import APIRouter, Depends, HTTPException, Header, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from models import User
from datetime import datetime, timedelta
from user.user_schema import UserCreate, UserLogin, UserResponse, TokenResponse
from user.user_crud import (
    get_user_by_name, get_user_by_email, create_user,
    verify_password, change_user_password,
    get_user_coin, add_user_coin, subtract_user_coin,
)
from user.auth import create_access_token, decode_access_token
from user.util import generate_auth_code, store_auth_code, verify_auth_code, get_user_db, send_email_code, email_auth_codes

security = HTTPBearer()

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_user_db)):  # ✅ 여기부터 전부 get_user_db로 변경
    if get_user_by_name(db, user.user_name):
        raise HTTPException(status_code=400, detail="이미 사용 중인 이름입니다.")
    if get_user_by_email(db, user.user_email):
        raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")
    return create_user(db, user.user_name, user.user_email, user.password)

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_user_db)):
    db_user = get_user_by_name(db, user.user_name)
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 잘못되었습니다.")
    
    token = create_access_token({"sub": str(db_user.user_id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(authorization: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_user_db)):
    # HTTPAuthorizationCredentials에서 토큰 추출
    token = authorization.credentials  # 여기서 credentials를 사용하여 JWT 토큰을 추출
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")

    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.user_id == user_id).first()
    return user

@router.post("/send-auth-code")
def send_auth_code(user_email: str):
    # 기존 인증 코드가 만료되었는지 확인하고, 만료되었으면 새로 발송
    if user_email in email_auth_codes and email_auth_codes[user_email]['expiration'] > datetime.now():
        raise HTTPException(status_code=400, detail="인증 코드가 아직 유효합니다.")
    
    code = generate_auth_code()
    expiration_time = datetime.now() + timedelta(minutes=10)  # 10분 유효
    store_auth_code(user_email, code, expiration_time)
    send_email_code(user_email, code)  # 실제 메일 발송
    return {"message": "인증 코드가 이메일로 전송되었습니다."}

@router.post("/resend-auth-code")
def resend_auth_code(user_email: str):

    code = generate_auth_code()
    expiration_time = datetime.now() + timedelta(minutes=1)  # 10분 유효

    store_auth_code(user_email, code, expiration_time)
    send_email_code(user_email, code)  # 실제 메일 발송
    
    return {"message": "새 인증 코드가 이메일로 전송되었습니다."}

@router.post("/verify-id-and-send-auth-code")
def verify_id_and_send_auth_code(user_name: str, user_email: str, db: Session = Depends(get_user_db)):
    # user_id로 사용자 조회
    user = db.query(User).filter(User.user_name == user_name).first()

    if not user:
        raise HTTPException(status_code=404, detail="존재하지 않는 사용자 ID입니다.")
    
    if user.user_email != user_email:
        raise HTTPException(status_code=400, detail="이메일이 사용자 ID와 일치하지 않습니다.")
    
    if user_email in email_auth_codes and email_auth_codes[user_email]['expiration'] > datetime.now():
        raise HTTPException(status_code=400, detail="인증 코드가 아직 유효합니다.")
    
    # 인증 코드 발급
    code = generate_auth_code()
    expiration_time = datetime.now() + timedelta(minutes=10)
    store_auth_code(user_email, code, expiration_time)
    send_email_code(user_email, code)

    return {"message": "인증 코드가 이메일로 전송되었습니다."}

@router.post("/verify-auth-code")
def verify_email_code(user_email: str, code: str):
    if verify_auth_code(user_email, code):
        return {"message": "이메일 인증 성공!"}
    raise HTTPException(status_code=400, detail="인증 코드가 올바르지 않습니다.")

@router.post("/reset-password")
def reset_password(user_email: str, new_password: str, db: Session = Depends(get_user_db)):
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    return change_user_password(db, user.user_id, new_password)

@router.post("/change-password")
def change_password(old_password: str, new_password: str, authorization: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_user_db)):
    token = authorization.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")
    
    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.user_id == user_id).first()
    if not verify_password(old_password, user.password_hash):
        raise HTTPException(status_code=401, detail="기존 비밀번호가 일치하지 않습니다.")
    
    return change_user_password(db, user_id, new_password)

@router.get("/coin")
def get_my_coin(authorization: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_user_db)):
    user_id = decode_access_token(authorization.credentials).get("sub")
    coin = get_user_coin(db, int(user_id))
    return {"coin": coin}

@router.post("/coin/add")
def add_coin(amount: int = Body(...), authorization: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_user_db)):
    user_id = decode_access_token(authorization.credentials).get("sub")
    user = add_user_coin(db, int(user_id), amount)
    return {"message": f"{amount} 코인 추가됨", "coin": user.coin}

@router.post("/coin/subtract")
def subtract_coin(amount: int = Body(...), authorization: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_user_db)):
    user_id = decode_access_token(authorization.credentials).get("sub")
    try:
        user = subtract_user_coin(db, int(user_id), amount)
        return {"message": f"{amount} 코인 차감됨", "coin": user.coin}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/profile/select")
def select_profile(
    profile_id: int = Body(...),
    profile_url: str = Body(...),
    db: Session = Depends(get_user_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user_id = decode_access_token(credentials.credentials).get("sub")
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저가 없습니다")

    user.profile_id = profile_id
    user.profile_url = profile_url
    db.commit()
    return {"message": "프로필이 저장되었습니다", "profile_id": profile_id, "profile_url": profile_url}

@router.get("/profile/me")
def get_my_profile(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_user_db)):
    user_id = decode_access_token(credentials.credentials).get("sub")
    user = db.query(User).filter(User.user_id == user_id).first()
    return {
        "profile_id": user.profile_id,
        "profile_url": user.profile_url
    }