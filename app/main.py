from fastapi import FastAPI

from app.api.routers.auth import router as auth_router
from app.api.routers.user import router as user_router
from app.db.base import initialize_tortoise

app = FastAPI()


app.include_router(auth_router)
app.include_router(user_router)
initialize_tortoise(app)
