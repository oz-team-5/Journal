from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DiaryCreate(BaseModel):
    """일기 작성 모델"""
    title: str = Field(..., max_length=200, description="일기 제목")
    content: str = Field(..., min_length=1, description="일기 내용")

# 일기 수정 (제목, 내용 둘중하나 수정할때는 Optional)
class DiaryUpdate(BaseModel):
    """일기 수정 모델"""
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = Field(None, min_length=1)

class DiaryResponse(BaseModel):
    """일기 조회 모델"""
    id: int #일기 id
    user_id: int
    title: str
    content: str
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True # Tortoise -> Pydantic 변환해주는 설정(orm mode = True)