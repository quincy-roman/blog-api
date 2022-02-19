from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from models import ALGORITHM, SECRET_KEY, UserInDB
from passlib.context import CryptContext

from services import find_one

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_hash(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


async def authenticate_user(collection: str, username: str, password: str):
    user: UserInDB = await find_one(collection, {'username': username})
    user = UserInDB(**user)
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
