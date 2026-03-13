from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.models.user import User
from app.schemas.quote import QuoteResponse
from app.services.auth import get_current_user  # 작성하신 auth 서비스 활용
from app.services.bookmark_service import bookmark_service

router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])


@router.post("/{quote_id}", status_code=status.HTTP_200_OK)
async def toggle_bookmark(
        quote_id: int,
        current_user: User = Depends(get_current_user)
):
    """
    명언 북마크 토글:
    - 북마크가 없으면 생성, 있으면 삭제
    """
    is_added, message = await bookmark_service.toggle_bookmark(current_user, quote_id)

    if is_added is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )

    return {"is_added": is_added, "message": message}


@router.get("/", response_model=List[QuoteResponse])
async def get_my_bookmarks(current_user: User = Depends(get_current_user)):
    """
    로그인한 현재 사용자가 저장한 명언 목록을 반환
    """
    return await bookmark_service.get_my_bookmarks(current_user)