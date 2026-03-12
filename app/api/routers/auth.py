from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import oauth2_scheme
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserResponse
from app.services.auth import (
    blacklist_token,
    create_user,
    get_current_user,
    login,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def user_login(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    return await login(form.username, form.password)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    token: str = Depends(oauth2_scheme), current_user: User = Depends(get_current_user)
):
    await blacklist_token(token, current_user)
    return {"message": "Logged out successfully"}


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(request: UserCreate) -> UserResponse:
    return await create_user(request)


@router.get("/me")
async def me(current_user: User = Depends(get_current_user)) -> dict:
    return {
        "id": current_user.id,
        "username": current_user.username,
        "created_at": current_user.created_at,
    }


@router.get("/check")
async def check_auth(current_user: User = Depends(get_current_user)) -> dict:
    return {
        "authenticated": True,
        "user_id": current_user.id,
        "username": current_user.username,
    }
