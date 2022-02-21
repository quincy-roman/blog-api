from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from models import ALGORITHM, SECRET_KEY, UserInDB
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_hash(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


async def authenticate_user(username: str, password: str):
    user = await UserInDB.by_username(username)
    if not user:
        return False
    if not verify_hash(password, user.hashed_pass):
        return False

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt
