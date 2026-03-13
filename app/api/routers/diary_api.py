from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.diary import DiaryCreate, DiaryResponse, DiaryUpdate
from app.services.auth import get_current_user
from app.services.diary_crud import (
    create_diary,
    delete_diary,
    get_diaries,
    update_diary,
)

router = APIRouter(prefix="/diaries", tags=["Diary"])


# 일기 작성
@router.post("", response_model=DiaryResponse)
async def api_create_diary(
    payload: DiaryCreate, current_user=Depends(get_current_user)
):
    return await create_diary(user_id=current_user.id, **payload.model_dump())


# 일기 목록 조회
@router.get("", response_model=List[DiaryResponse])
async def api_get_diaries(current_user=Depends(get_current_user)):
    return await get_diaries(user_id=current_user.id)


# 일기 수정
@router.put("/{diary_id}")
async def api_update_diary(
    diary_id: int, payload: DiaryUpdate, current_user=Depends(get_current_user)
):

    update_data = payload.model_dump(exclude_unset=True)
    # 사용자가 수정한 부분만 수정
    success = await update_diary(
        diary_id=diary_id, user_id=current_user.id, **update_data
    )
    if not success:
        raise HTTPException(
            status_code=403, detail="수정 실패 : 권한이 없거나 일기가 없습니다."
        )
    return {"message": "success"}


# 일기 삭제
@router.delete("/{diary_id}")
async def api_delete_diary(diary_id: int, current_user=Depends(get_current_user)):
    success = await delete_diary(diary_id=diary_id, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=403, detail="삭제 실패 : 권한이 없거나 일기가 없습니다."
        )
    return {"message": "success"}
