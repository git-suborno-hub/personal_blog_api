from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ArticleCreate(BaseModel):
    title=str
    content=str
    tags: Optional[List[str]] = None
    is_published: bool = False

class ArticleResponse(BaseModel):
    id: int 
    title: str
    content: str
    tags: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime
    is_published: bool

    class Config:
        from_attributes=True