import asyncio
import logging
from contextlib import asynccontextmanager  # 비동기 자원을 안전하게 관리하기 위한 도구

import uvicorn
from fastapi import FastAPI

from app.api.routers import diary_api, quote
from app.api.routers.auth import router as auth_router
from app.api.routers.user import router as user_router
from app.db.base import initialize_tortoise
from app.scraping.quote_scraper import quote_scraper  # 스크래퍼 가져오기

# 1. 로깅 기본 설정 (메시지 및 출력 형식)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# 2. 서버 수명 주기(Lifespan) 정의
@asynccontextmanager
async def lifespan(app: FastAPI):
    # [시작 시 작업]
    logger.info("서버 시작")

    # DB 초기화 및 테이블 생성이 완료된 후 스크래핑을 실행하기 위해
    # 스크래핑 작업을 백그라운드 태스크로 예약
    # 이렇게 하면 서버 부팅 속도에 영향을 주지않음
    logger.info("명언 데이터 동기화를 백그라운드에서 시작")
    asyncio.create_task(quote_scraper.fetch_and_save_quotes(max_pages=5))

    yield  # 서버 가동 (사용자 요청 수신)

    # [종료 시 작업]
    logger.info("서버 종료")


# 3. FastAPI 앱 생성 및 lifespan 등록
app = FastAPI(lifespan=lifespan)

# 4. 라우터 등록
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(quote.router)

app.include_router(diary_api.router)

# 5. DB 설정 초기화
initialize_tortoise(app)

if __name__ == "__main__":
    # 로컬 개발 환경 실행 설정
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
