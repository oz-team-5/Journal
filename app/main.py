import uvicorn
from fastapi import FastAPI

from app.api.routers.auth import router as auth_router
from app.api.routers.user import router as user_router
from app.db.base import initialize_tortoise

from app.api.v1 import quote

app = FastAPI()


app.include_router(auth_router)
app.include_router(user_router)
initialize_tortoise(app)
app.include_router(quote.router, prefix="/api/v1")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
