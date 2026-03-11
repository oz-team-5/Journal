from fastapi import APIRouter, status

from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.user import delete_user, get_user, get_users, update_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get() -> User:
    return await get_users()


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_one(user_id: int) -> User:
    return await get_user(user_id)


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update(user_id: int, request: UserUpdate) -> User:
    return await update_user(user_id=user_id, request=request)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user_id: int) -> None:
    return await delete_user(user_id=user_id)
