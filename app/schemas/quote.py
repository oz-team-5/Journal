from pydantic import BaseModel, ConfigDict


class QuoteBase(BaseModel):
    content: str
    author: str = "Unknown"


class QuoteCreate(QuoteBase):
    pass


class QuoteResponse(QuoteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
