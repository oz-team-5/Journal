import asyncio
import logging
import random
import re

import httpx
from bs4 import BeautifulSoup

from app.models.quote import Quote

# 해당 모듈 전용 로거 생성
logger = logging.getLogger(__name__)


class QuoteScraper:
    def __init__(self):
        self.base_url = "https://saramro.com/quotes"
        self.last_page = 0

    async def fetch_and_save_quotes(self, max_pages: int = 3):
        all_scraped_data = []
        star_page = self.last_page + 1

        async with httpx.AsyncClient() as client:
            headers = {"User-Agent": "Mozilla/5.0"}

            for page in range(star_page, star_page + max_pages):
                current_url = f"{self.base_url}?page={page}"
                logger.info(f"{page}페이지 스캔 시작: {current_url}")

                try:
                    response = await client.get(current_url, headers=headers)
                    if response.status_code != 200:
                        logger.warning(
                            f"{page}페이지 응답 오류 (상태 코드: {response.status_code})"
                        )
                        break

                    soup = BeautifulSoup(response.text, "html.parser")
                    rows = soup.select("table tr")

                    if not rows:
                        logger.info(
                            f"{page}페이지에서 더 이상 데이터를 찾을 수 없습니다."
                        )
                        break

                    for row in rows:
                        td = row.select_one("td")
                        if not td:
                            continue

                        raw_text = td.get_text(separator="\n", strip=True)
                        lines = [
                            line.strip()
                            for line in raw_text.split("\n")
                            if line.strip()
                        ]

                        if len(lines) >= 2:
                            content = lines[0]
                            author = lines[1].lstrip("-").strip()

                            # 한글 패턴 검사 (re 모듈 활용)
                            if re.search(r"[가-힣]", content):
                                all_scraped_data.append(
                                    {"content": content, "author": author}
                                )

                    # 마지막 스크랩 페이지 저장
                    self.last_page = page

                    if page < max_pages:
                        delay = random.uniform(1.0, 2.5)
                        logger.debug(
                            f"서버 부하 방지를 위해 {delay:.2f}초간 대기합니다."
                        )
                        await asyncio.sleep(delay)

                except Exception:
                    logger.error(f"{page}페이지 처리 중 예외 발생", exc_info=True)
                    break

        if not all_scraped_data:
            logger.info("새로 수집된 명언 데이터가 없습니다.")
            return 0

        # 중복 확인 및 벌크 저장 로직
        scraped_contents = [item["content"] for item in all_scraped_data]
        existing_records = await Quote.filter(content__in=scraped_contents).values_list(
            "content", flat=True
        )

        new_quotes = [
            Quote(content=item["content"], author=item["author"])
            for item in all_scraped_data
            if item["content"] not in existing_records
        ]

        if new_quotes:
            await Quote.bulk_create(new_quotes)
            logger.info(f"새로운 명언 {len(new_quotes)}개를 성공적으로 저장했습니다.")
        else:
            logger.info("모든 데이터가 이미 존재하여 새로 저장할 명언이 없습니다.")

        return len(new_quotes)


quote_scraper = QuoteScraper()
