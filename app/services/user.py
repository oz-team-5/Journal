from fastapi import status
from fastapi.exceptions import HTTPException

from app.models.user import User
from app.schemas.user import UserUpdate
from app.services.auth import get_password_hash


async def get_users() -> list[User]:
    users = await User.all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
        )
    return users


async def get_user(user_id: int) -> User:
    user = await User.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


async def update_user(user_id: int, request: UserUpdate) -> User:
    user = await User.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if request.username:
        username_valid = await User.get_or_none(username=request.username)
        if username_valid and username_valid.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
        user.username = request.username

    if request.password:
        user.password_hash = get_password_hash(request.password)

    await user.save()
    return user


async def delete_user(user_id: int) -> None:
    user = await User.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    await user.delete()
    return None
