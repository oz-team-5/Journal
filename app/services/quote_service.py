import random
from typing import List, Optional

from app.models.quote import Quote
from app.scraping.quote_scraper import quote_scraper  # 이전에 만든 스크래퍼


class QuoteService:
    # 1. 랜덤 명언 가져오기
    async def get_random_quote(self) -> Optional[Quote]:
        count = await Quote.all().count()
        if count == 0:
            return None
        index = random.randint(0, count - 1)
        return await Quote.all().offset(index).first()

    # 2. 명언 목록 조회 (페이징 처리가 가능하도록)
    async def get_quotes(self, skip: int = 0, limit: int = 10) -> List[Quote]:
        return await Quote.all().offset(skip).limit(limit)

    # 3. 웹에서 명언 동기화 (벌크 로직 통합)
    async def sync_quotes_from_web(self,max_pages:int = 3) -> int:
        # 스크래퍼를 통해 외부 데이터 긁어오기
        new_count = await quote_scraper.fetch_and_save_quotes(max_pages)
        return new_count



quote_service = QuoteService()
