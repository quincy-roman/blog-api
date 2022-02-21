from typing import Optional

from fastapi import FastAPI

from db.connection import init
from routers import blog_router, user_router

app = FastAPI()


@app.on_event('startup')
async def app_init():
    # Initialize beanie
    await init()

    # Add your routers
    app.include_router(blog_router.router)
    app.include_router(user_router.router)
