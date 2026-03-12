from fastapi import APIRouter, HTTPException, status

from app.schemas.quote import QuoteCreate, QuoteResponse
from app.services.quote_service import quote_service

router = APIRouter(prefix="/quotes", tags=["Quotes"])


@router.get("/random", response_model=QuoteResponse, summary="랜덤 명언 조회")
async def get_random_quote():
    quote = await quote_service.get_todays_quote()

    # 1. 데이터가 없을 경우에 대한 예외 처리 추가!
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No quotes found. Please sync first.",
        )

    return quote


@router.post("/", response_model=QuoteResponse, summary="명언 직접 등록")
async def create_quote(quote_in: QuoteCreate):
    return await quote_service.add_new_quote(quote_in)


# --- 아래 엔드포인트를 추가해야 테스트가 통과됩니다 ---
@router.post("/sync", status_code=status.HTTP_201_CREATED, summary="명언 데이터 동기화")
async def sync_quotes():
    """
    외부 사이트에서 명언을 스크래핑하여 DB에 저장합니다.
    """
    # quote_service에 sync_quotes_from_web() 같은 메서드가 있다고 가정합니다.
    count = await quote_service.sync_quotes_from_web()
    return {"message": f"Successfully synced {count} quotes."}
