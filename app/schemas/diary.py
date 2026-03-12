from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DiaryBase(BaseModel):
    """중복되는 필드 묶어서 상속하기"""

    title: str = Field(..., max_length=200, description="일기 제목")
    content: str = Field(..., min_length=1, description="일기 내용")


class DiaryCreate(DiaryBase):
    """일기 작성 모델"""

    pass


# 일기 수정 (제목, 내용 둘중하나 수정할때는 Optional)
class DiaryUpdate(BaseModel):
    """일기 수정 모델"""

    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = Field(None, min_length=1)


class DiaryResponse(DiaryBase):
    """일기 조회 모델"""

    id: int  # 일기 id
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    # v2로 수정완료
