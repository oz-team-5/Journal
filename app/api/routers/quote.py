from fastapi import APIRouter, HTTPException, status

from app.schemas.quote import QuoteResponse
from app.services.quote_service import quote_service

router = APIRouter(prefix="/quotes", tags=["quote"])


@router.get("/random", response_model=QuoteResponse, summary="랜덤 명언 조회")
async def get_random_quote():
    """
    DB에 저장된 명언 중 하나를 무작위로 선택하여 반환합니다.
    """
    quote = await quote_service.get_random_quote()

    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="조회 가능한 명언이 없습니다. 먼저 동기화를 진행해주세요.",
        )

    return quote


@router.post("/sync", status_code=status.HTTP_200_OK, summary="명언 데이터 수동 동기화")
async def sync_quotes(max_pages: int = 3):
    """
    웹 사이트에서 최신 명언을 긁어와 DB를 업데이트합니다.
    서버 재시작 없이 데이터를 보충하고 싶을 때 사용합니다.
    """
    try:
        count = await quote_service.sync_quotes_from_web(max_pages=max_pages)

        if count == 0:
            return {"message": "이미 최신 상태입니다. 새로 추가된 데이터가 없습니다."}

        return {
            "message": f"동기화가 완료되었습니다. {count}개의 명언이 새로 추가되었습니다."
        }

    except Exception as e:
        # 동기화 중 발생한 에러를 클라이언트에게 알림
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"동기화 중 오류가 발생했습니다: {str(e)}",
        )
