from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List


class ArticleBase(BaseModel):
    title: str
    content: str
    tags: Optional[str] = Field(default_factory=list)


class ArticleCreate(ArticleBase):
    pass


class ArticleResponse(ArticleBase):
    id: int
    created_at: datetime
    author: str = "Anonymous"  # models.py এর সাথে মিল রাখার জন্য

    model_config = ConfigDict(
        from_attributes=True,          # SQLAlchemy object → Pydantic (আগের from_orm=True)
        # json_encoders={datetime: lambda v: v.isoformat()}  # optional
    )