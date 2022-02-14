import os
from typing import Optional

from pydantic import BaseModel

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
