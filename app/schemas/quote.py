from pydantic import BaseModel, ConfigDict


class QuoteCreate(BaseModel):
    content: str
    author: str = "Unknown"


class QuoteResponse(QuoteCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
