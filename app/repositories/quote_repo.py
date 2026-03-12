from typing import List, Optional

from app.models.quote import Quote
from app.schemas.quote import QuoteCreate


class QuoteRepository:
    """명언 데이터베이스에 직접 접근하는 클래스"""

    @staticmethod
    async def create(quote_in: QuoteCreate) -> Quote:
        """새로운 명언을 저장합니다."""
        return await Quote.create(**quote_in.model_dump())

    @staticmethod
    async def get_by_id(quote_id: int) -> Optional[Quote]:
        """ID로 특정 명언을 조회합니다."""
        return await Quote.get_or_none(id=quote_id)

    @staticmethod
    async def get_all() -> List[Quote]:
        """모든 명언 목록을 반환합니다."""
        return await Quote.all()

    @staticmethod
    async def get_random() -> Optional[Quote]:
        """(예시) 랜덤으로 명언 하나를 가져오는 복잡한 로직"""
        # Tortoise ORM의 raw SQL이나 특수 쿼리를 여기에 작성
        return await Quote.first()  # 여기서는 단순화하여 첫 번째 데이터를 반환


# 싱글톤 패턴으로 인스턴스화하여 제공 (선택 사항)
quote_repo = QuoteRepository()
