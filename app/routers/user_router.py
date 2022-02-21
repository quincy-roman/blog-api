from datetime import timedelta
from typing import List

from dependencies import get_current_active_user
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from models import ACCESS_TOKEN_EXPIRE_MINUTES, Token, User, UserInDB
from services import authenticate_user, create_access_token, get_password_hash

router = APIRouter(tags=['users'])

BAD_LOGIN = HTTPException(400, 'Incorrect username or password', {
                          "WWW-Authenticate": "Bearer"})


@router.get('/users', response_description='Get all users', response_model=List[User])
async def get_all_users(limit: int = 100):
    users = await UserInDB.find_all(limit=limit).to_list()

    return users


@router.post('/register', response_description='Register a new user', response_model=User, status_code=201)
async def create_user(user: UserInDB = Body(...)):
    potential_user = await UserInDB.by_username(user.username)
    if potential_user is not None:
        raise HTTPException(409, "User with that username already exists")

    user.hashed_pass = get_password_hash(user.hashed_pass)
    created_user = await user.insert()

    return created_user


@router.post('/token', response_model=Token)
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user: UserInDB = await authenticate_user(form_data.username, form_data.password)
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
