from fastapi import APIRouter, HTTPException
from app.services.question_service import question_service

router = APIRouter(prefix="/question", tags=["question"])


@router.get("/random", summary="무작위 성찰 질문 조회")
async def get_random_question():
    """
    서버 메모리에 저장된 질문 리스트 중 하나를 던져줍니다.
    DB를 사용하지 않아 매우 빠릅니다.
    """
    question = await question_service.get_random_question()

    if not question:
        raise HTTPException(status_code=404, detail="질문 목록이 비어 있습니다.")

    return {"question": question}