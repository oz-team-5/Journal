# from app.services.auth import get_current_user
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse 
from app.services.diary_crud import(
    create_diary,
    get_diaries,
    update_diary,
    delete_diary,
)

router = APIRouter()

# ### 테스트용 임시 Get_current_user함수
# async def get_current_user():
#     class FakeUser:
#         id = 1
        
#     return FakeUser()
# ###

# 일기 작성
@router.post("/diaries", response_model=DiaryResponse)
async def api_create_diary(
    payload: dict,
    current_user = Depends(get_current_user)
):
    return await create_diary(
        user_id=current_user.id,
        title=payload.get("title"),
        content=payload.get("content")
    )

# 일기 목록 조회
@router.get("/diaries")
async def api_get_diaries(current_user = Depends(get_current_user)):
    return await get_diaries(user_id=current_user.id)

# 일기 수정
@router.put("/diaries/{diary_id}")
async def api_update_diary(
    diary_id: int, 
    payload: dict,
    current_user = Depends(get_current_user)
):
    
    real_id = current_user.id

    success = await update_diary(
        diary_id=diary_id,
        user_id=real_id,
        title=payload.get("title"),
        content=payload.get("content")
    )
    if not success:
        raise HTTPException(status_code=404, detail="수정 실패 : 권한이 없거나 일기가 없습니다.")
    return {"message" : "success"}

#일기 삭제
@router.delete("/diaries/{diary_id}")
async def api_delete_diary(
    diary_id: int,
    current_user = Depends(get_current_user)
):
    success = await delete_diary(diary_id=diary_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="삭제 실패 : 권한이 없거나 일기가 없습니다.")
    return {"message" : "success"}
 