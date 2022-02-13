from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from models import User, UserInDB
from services import *

router = APIRouter()
collection = 'users'


@router.get('/', response_description='Get all users', response_model=User)
async def get_all_users(limit: int = 100):
    users = await find_all(collection, None, limit)

    return JSONResponse(status_code=200, content=users)


@router.post('/register', response_description='Register a new user', response_model=User)
async def create_user(user: UserInDB = Body(...)):
    user.hashed_pass = get_password_hash(user.hashed_pass)
    created_user = await insert(collection, user)

    return JSONResponse(created_user, 201)
