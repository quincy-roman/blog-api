from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.services.blog_service import find_one
from models import ALGORITHM, SECRET_KEY, TokenData, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(401, 'Could not validate credentials',
                                          {'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = find_one({'username': token_data.username})
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(400, 'Inactive user')
    return current_user
