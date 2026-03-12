import pytest
from httpx import AsyncClient, ASGITransport
from tortoise import Tortoise
from app.main import app
import os


@pytest.fixture(scope="module", autouse=True)
async def initialize_tests():
    db_path = "test.sqlite3"

    # 1. 이전 테스트의 잔여물이 있다면 삭제
    if os.path.exists(db_path):
        os.remove(db_path)

    # 2. 메모리 대신 '파일'에 DB와 테이블 생성
    await Tortoise.init(
        db_url=f"sqlite://{db_path}",
        modules={"models": ["app.models.quote"]}
    )
    await Tortoise.generate_schemas()

    yield  # 테스트 실행

    # 3. 테스트 종료 후 연결 해제 및 임시 파일 삭제
    await Tortoise.close_connections()
    if os.path.exists(db_path):
        os.remove(db_path)


# 1. 클라이언트를 생성하는 Fixture 정의
@pytest.fixture
async def client():
    # ASGITransport를 통해 FastAPI 앱을 연결합니다.
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver"
    ) as ac:
        yield ac


# 2. 테스트 코드 (fixture인 'client'를 인자로 받음)
@pytest.mark.asyncio
async def test_read_random_quote_success(client: AsyncClient):
    # 이제 'app' 인자 오류 없이 정상 작동합니다.
    response = await client.get("/api/v1/quotes/random")

    # DB에 데이터가 있을 경우와 없을 경우를 나누어 검증
    if response.status_code == 200:
        data = response.json()
        assert "content" in data
        assert "author" in data
    else:
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_sync_quotes(client: AsyncClient):
    response = await client.post("/api/v1/quotes/sync")
    assert response.status_code == 201
    assert "message" in response.json()