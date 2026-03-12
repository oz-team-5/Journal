# app/db/base.py 수정본
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import settings

TORTOISE_MODELS = [
    "app.models.user",
    "app.models.diary",
    "app.models.quote",
    "app.models.bookmark",
    "app.models.question",
    "app.models.user_question",
    "aerich.models",
    "app.models.auth",
]

TORTOISE_ORM = {
    "connections": {
        "default": settings.DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": TORTOISE_MODELS,
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "Asia/Seoul",
}


def initialize_tortoise(app: FastAPI) -> None:
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=False,
    )
