from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.auth import get_current_user
from app.services.user import delete_user, get_user, get_users, update_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get() -> list[User]:
    return await get_users()


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_one(user_id: int) -> User:
    return await get_user(user_id)


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update(
    user_id: int,
    request: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인 계정만 수정할 수 있습니다.",
        )
    return await update_user(user_id=user_id, request=request)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    user_id: int, current_user: Annotated[User, Depends(get_current_user)]
) -> None:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인 계정만 삭제할 수 있습니다.",
        )
    return await delete_user(user_id=user_id)
