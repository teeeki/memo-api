from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bcrypt

from app.config.database import Base, User, get_db
from app.config.jwt import (
    create_hashed_password,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])

""" モデルスキーマ """
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    """ ログインリクエスト """
    username: str
    password: str

class SignupRequest(BaseModel):
    """ ユーザ登録リクエスト """
    username: str
    password: str

class UserResponse(BaseModel):
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