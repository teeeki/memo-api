from datetime import datetime, timedelta, timezone
import hashlib
from typing import Union

from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic import BaseModel
from passlib.context import CryptContext

SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

''' ハッシュ値関連 '''
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_hashed_password(password):
    """ハッシュ値生成"""
    sha = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pwd_context.hash(sha)


def verify_password(password, hashed_password):
    """ハッシュ値検証"""
    sha = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pwd_context.verify(sha, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta):
    """ アクセストークンの作成 """
    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)