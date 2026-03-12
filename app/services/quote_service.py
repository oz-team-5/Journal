from app.repositories.quote_repo import quote_repo  # 인스턴스를 가져옵니다
from app.scraping.quote_scraper import quote_scraper  # 인스턴스를 가져옵니다


class QuoteService:
    def __init__(self):
        self.quote_repo = quote_repo
        self.scraper = quote_scraper

    async def get_todays_quote(self):
        return await self.quote_repo.get_random()

    async def sync_quotes_from_web(self):
        # 이름 불일치 문제 해결: fetch_and_save_quotes() 호출
        # 스크래퍼 내부에 이미 DB 저장 및 중복 방지 로직이 있으므로 이 한 줄로 끝납니다!
        count = await self.scraper.fetch_and_save_quotes()
        return count


# 라우터에서 사용할 싱글톤 인스턴스
quote_service = QuoteService()
