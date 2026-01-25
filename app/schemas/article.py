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


class ArticleResponse(ArticleBase):
    id: int
    created_at: datetime
    # author: str = "Anonymous"  # models.py এর সাথে মিল রাখার জন্য
    author: str 
    tags: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,          # SQLAlchemy object → Pydantic (আগের from_orm=True)
        # json_encoders={datetime: lambda v: v.isoformat()}  # optional
    )

class PaginatedArticleResponse(BaseModel):
    items: List[ArticleResponse]
    total: int
    limit: int
    offset: int