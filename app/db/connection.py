import os

from beanie import init_beanie
from models import Blog, UserInDB
from motor.motor_asyncio import AsyncIOMotorClient


async def init():
    """Initialize beanie ODM with MongoDB"""
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client.blogs

    await init_beanie(database=db, document_models=[Blog, UserInDB])
