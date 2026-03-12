from fastapi import FastAPI
from app.db.base import initialize_tortoise
from app.routers import diary_api

app = FastAPI()

app.include_router(diary_api.router)

initialize_tortoise(app)