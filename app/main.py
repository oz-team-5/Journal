import uvicorn
from fastapi import FastAPI

from app.db.base import initialize_tortoise

from app.api.v1 import quote

app = FastAPI()

initialize_tortoise(app)
app.include_router(quote.router, prefix="/api/v1")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
