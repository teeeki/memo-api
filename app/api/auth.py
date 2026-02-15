from datetime import timedelta
from app.config.model_config import ModelConfig
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bcrypt

from app.config.database import Base, User, get_db
from app.config.jwt import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_hashed_password,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])

""" モデルスキーマ """
class Token(ModelConfig):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(ModelConfig):
    """ ログインリクエスト """
    username: str
    password: str

class SignupRequest(ModelConfig):
    """ ユーザ登録リクエスト """
    username: str
    password: str

class UserResponse(ModelConfig):
    """
    ユーザー情報のレスポンスモデル
    ユーザ登録リクエストと同時に使用
    """
    id: int
    username: str
    
""" モデルスキーマ """

""" ユーザー認証系 """
# ユーザー登録
@router.post("/signup")
async def create_user(signup_user: SignupRequest, db: Session = Depends(get_db)):
    # 既存チェック
    exist_user = db.query(User).filter(User.password == signup_user.password).first()
    print("Password bytes:", len(signup_user.password.encode('utf-8')))

    if exist_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = create_hashed_password(signup_user.password)

    try:
        db.add(User(username=signup_user.username, password=hashed_password))
        db.commit()
        return {"msg": "user created"}
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"DB error: {str(e.orig)}",
    )

# ログイン
@router.post("/login", response_model=Token)
async def login(login_user: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_user.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not verify_password(login_user.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}