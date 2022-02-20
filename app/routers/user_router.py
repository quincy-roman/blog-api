from datetime import timedelta

from dependencies import get_current_active_user
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from models import ACCESS_TOKEN_EXPIRE_MINUTES, Token, User, UserInDB
from services import *

router = APIRouter(tags=['users'])

collection = 'users'
BAD_LOGIN = HTTPException(400, 'Incorrect username or password', {
                          "WWW-Authenticate": "Bearer"})


@router.get('/users', response_description='Get all users', response_model=User)
async def get_all_users(limit: int = 100):
    users = await find_all(collection, None, limit)

    return JSONResponse(status_code=200, content=users)


@router.post('/register', response_description='Register a new user', response_model=User)
async def create_user(user: UserInDB = Body(...)):
    user.hashed_pass = get_password_hash(user.hashed_pass)
    created_user = await insert(collection, user)

    return JSONResponse(created_user, 201)


@router.post('/token', response_model=Token)
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user: UserInDB = await authenticate_user(collection, form_data.username, form_data.password)
    if not user:
        raise BAD_LOGIN

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': f'username:{user.username}'}, expires_delta=access_token_expires
    )

    # * Note: JWT IDs can collide so prefixing sub with whatever the thing is is helpful.
    # ! It must be unique across the ENTIRE application, and needs to be a string

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/users/me', response_model=User)
async def read_me(current_user: User = Depends(get_current_active_user)):
    return current_user
