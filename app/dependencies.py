from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from models import ALGORITHM, SECRET_KEY, TokenData, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
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

    # Use a User object to avoid storing the password hash unnecessarily.
    # Taking a slice of token_data.username because of appended "username:"
    # user = User(**await find_one('users', {'username': token_data.username[9:]}))
    user = await User.find_one(User.username == token_data.username[9:])

    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.disabled:
        raise HTTPException(400, 'Inactive user')
    return current_user
