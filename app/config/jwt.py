from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from passlib.context import CryptContext


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    

''' ハッシュ値関連 '''
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_hashed_password(password):
    """ハッシュ値生成"""
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    """ハッシュ値検証"""
    return pwd_context.verify(password, hashed_password)