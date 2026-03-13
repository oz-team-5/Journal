import asyncio
import httpx
from bs4 import BeautifulSoup
import re  # 한글 판독기를 위한 마법 도구 추가!


async def scrape_only_korean_quotes():
    url = "https://saramro.com/quotes"
    print(f"🌐 '{url}' 사이트에 접속합니다...")

    scraped_data_list = []

    async with httpx.AsyncClient() as client:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = await client.get(url, headers=headers)

        if response.status_code != 200:
            print("❌ 데이터를 가져오는 데 실패했습니다.")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select("table tr")

        for row in rows:
            td = row.select_one("td")
            if not td:
                continue

            # <br/>을 기준으로 텍스트를 줄바꿈(\n)으로 분리합니다.
            raw_text = td.get_text(separator="\n", strip=True)

            # 빈 줄을 제외하고 진짜 글씨가 있는 줄만 리스트로 만듭니다.
            lines = [line.strip() for line in raw_text.split("\n") if line.strip()]

            # 보통 1번째 줄(lines[0])이 명언, 2번째 줄(lines[1])이 작가입니다.
            if len(lines) >= 2:
                content = lines[0]
                author = lines[1].lstrip("-").strip()

                # 🚨 핵심 마법: 명언 내용에 한글(가~힣)이 포함되어 있는지 검사합니다!
                if re.search(r'[가-힣]', content):
                    scraped_data_list.append({
                        "content": content,
                        "author": author
                    })

    print(f"✅ 영어를 쏙 빼고, 총 {len(scraped_data_list)}개의 '한글 명언'만 챙겼습니다!\n")
    return scraped_data_list


async def main():
    result_list = await scrape_only_korean_quotes()

    print("================ [ 수집된 한글 명언 리스트 ] ================")
    for idx, item in enumerate(result_list, 1):
        print(f"{idx}. {item['content']} - {item['author']}")
    print("=============================================================")


if __name__ == "__main__":
    asyncio.run(main())