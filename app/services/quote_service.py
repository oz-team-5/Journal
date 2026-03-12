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
    async def sync_quotes_from_web(self) -> int:
        # 스크래퍼를 통해 외부 데이터 긁어오기
        scraped_data = await quote_scraper.scrape_korean_quotes()

        if not scraped_data:
            return 0

        # 중복 체크를 위해 현재 DB의 모든 명언 내용 가져오기 (성능 최적화)
        scraped_contents = [item["content"] for item in scraped_data]
        existing_contents = await Quote.filter(
            content__in=scraped_contents
        ).values_list("content", flat=True)

        # 중복되지 않은 새 명언만 객체로 생성
        new_quotes = [
            Quote(content=item["content"], author=item["author"])
            for item in scraped_data
            if item["content"] not in existing_contents
        ]

        # 벌크 저장 실행
        if new_quotes:
            await Quote.bulk_create(new_quotes)

        return len(new_quotes)


quote_service = QuoteService()