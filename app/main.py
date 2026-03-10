from fastapi import FastAPI

from app.db.base import initialize_tortoise

app = FastAPI()


initialize_tortoise(app)
