import httpx
from bs4 import BeautifulSoup
import re
from app.models.quote import Quote


# repository 패턴을 유지하고 싶다면 quote_repo를 가져와도 되지만,
# 성능 최적화를 위해 여기서는 ORM 모델(Quote)을 직접 사용하여 Bulk 처리를 합니다.

class QuoteScraper:
    def __init__(self):
        self.url = "https://saramro.com/quotes"

    async def fetch_and_save_quotes(self):
        print(f"🌐 '{self.url}'에서 한글 명언 스크래핑을 시작합니다...")

        # 1. 인터넷에서 데이터 긁어오기 (이전과 동일)
        async with httpx.AsyncClient() as client:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = await client.get(self.url, headers=headers)

            if response.status_code != 200:
                print("❌ 데이터를 가져오는 데 실패했습니다.")
                return 0

            soup = BeautifulSoup(response.text, "html.parser")
            rows = soup.select("table tr")

            scraped_data = []  # 임시 보관함

            for row in rows:
                td = row.select_one("td")
                if not td:
                    continue

                raw_text = td.get_text(separator="\n", strip=True)
                lines = [line.strip() for line in raw_text.split("\n") if line.strip()]

                if len(lines) >= 2:
                    content = lines[0]
                    author = lines[1].lstrip("-").strip()

                    # 한글 판독기! 한글이 포함된 명언만 챙깁니다.
                    if re.search(r'[가-힣]', content):
                        scraped_data.append({"content": content, "author": author})

        # =================================================================
        # 🚀 2. 여기서부터가 핵심! 성능을 100배 높여주는 Bulk Insert 로직
        # =================================================================
        if not scraped_data:
            return 0

        # 수집한 명언의 '내용(content)'만 쏙 빼서 리스트로 만듭니다.
        scraped_contents = [item["content"] for item in scraped_data]

        # 🚨 [최적화 1] DB에 "이 리스트에 있는 명언 중 네가 가진 거 다 불러와!"라고 딱 1번만 질문합니다.
        existing_records = await Quote.filter(content__in=scraped_contents).values_list("content", flat=True)

        # 파이썬 메모리 상에서 겹치는 것을 제외하고 새로운 명언만 박스(new_quotes)에 담습니다.
        new_quotes = []
        for item in scraped_data:
            if item["content"] not in existing_records:
                # DB에 바로 넣지 않고, 일단 객체(상자)로만 만들어 둡니다.
                new_quotes.append(Quote(content=item["content"], author=item["author"]))

        # 🚨 [최적화 2] 새로운 명언 상자들을 DB에 '한꺼번에 쏟아붓습니다' (단 1번의 쿼리!)
        if new_quotes:
            await Quote.bulk_create(new_quotes)
            print(f"✅ {len(new_quotes)}개의 새 명언을 DB에 성공적으로 저장했습니다!")
        else:
            print("✅ 새로운 명언이 없습니다. (모두 중복)")

        return len(new_quotes)


# 서비스에서 불러다 쓸 수 있도록 로봇 객체 생성
quote_scraper = QuoteScraper()