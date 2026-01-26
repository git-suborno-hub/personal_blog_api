from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List


class ArticleBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = Field(default=None, description="List of tags, e.g. ['python', 'fastapi']")
    author: Optional[str] = None


class ArticleCreate(ArticleBase):
    pass

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    tags: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     from_attributes = True  # এই line টি থাকতে হবে

class PaginatedArticleResponse(BaseModel):
    items: List[ArticleResponse]
    total: int
    limit: int
    offset: int

    model_config = ConfigDict(from_attributes=True)