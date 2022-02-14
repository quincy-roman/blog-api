from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from models import ACCESS_TOKEN_EXPIRE_MINUTES, User, UserInDB
from services import *

router = APIRouter()
collection = 'users'
BAD_LOGIN = HTTPException(400, 'Incorrect username or password', {
                          "WWW-Authenticate": "Bearer"})


@router.get('/', response_description='Get all users', response_model=User)
async def get_all_users(limit: int = 100):
    users = await find_all(collection, None, limit)

    return JSONResponse(status_code=200, content=users)


@router.post('/register', response_description='Register a new user', response_model=User)
async def create_user(user: UserInDB = Body(...)):
    user.hashed_pass = get_password_hash(user.hashed_pass)
    created_user = await insert(collection, user)

    return JSONResponse(created_user, 201)


@router.post('/token')
async def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user: UserInDB = await authenticate_user(collection, form_data.username, form_data.password)
    if not user:
        raise BAD_LOGIN

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )

    return {'access_token': access_token, 'token_type': 'bearer'}
