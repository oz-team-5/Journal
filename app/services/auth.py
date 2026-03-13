from datetime import timedelta
from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException

from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_password_hash,
    get_token_expired_at,
    get_user_id_from_token,
    oauth2_scheme,
    verify_password,
)
from app.models.auth import TokenBlacklist
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserResponse


async def blacklist_token(token: str, user: User) -> None:
    """토큰을 블랙리스트에 등록"""
    expired_at = get_token_expired_at(token)
    #
    print("blacklist start")
    print("token:", token)
    print("user_id:", user.id)
    print("expired_at:", expired_at)
    #

    exists = await TokenBlacklist.filter(token=token).exists()
    if exists:
        return
    #
    print("already exists:", exists)
    #
    await TokenBlacklist.create(
        token=token,
        user=user,
        expired_at=expired_at,
    )
    #
    saved = await TokenBlacklist.filter(token=token).exists()
    print("saved after create:", saved)
    #


async def get_user_by_id(user_id: int) -> User:
    """ID로 유저 조회"""
    user = await User.get_or_none(id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """로그인 사용자 조회"""

    user_id = get_user_id_from_token(token)

    if await TokenBlacklist.filter(token=token).exists():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been blacklisted",
        )

    return await get_user_by_id(user_id)


async def login(username: str, password: str) -> Token:
    user = await User.get_or_none(username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


async def create_user(request: UserCreate) -> UserResponse:
    user_valid = await User.get_or_none(username=request.username)
    if user_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    user = await User.create(
        username=request.username, password_hash=get_password_hash(request.password)
    )
    return UserResponse(username=user.username, created_at=user.created_at)
