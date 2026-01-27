from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List
from pydantic import field_validator


class ArticleBase(BaseModel):
    title: str = Field(
        ...,
        min_length=5,
        max_length= 100,
        description="Article title must be between 5 and 100 character."
    )
    content: str = Field(
        ...,
        min_length=10,
        description="Article content must be at least 10 characters long."
    )
    tags: Optional[List[str]] = Field(
        default= None,
        description="List of tags..."
    )
    author: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Author name"
    )
    
    @field_validator('title','content',mode='before')
    @classmethod
    def strip_whitespace(cls, value:str):
        if value is not None:
            stripped=value.strip()
            if not stripped:
                raise ValueError("This field cannot be empty or just whitespace")
            return stripped
        return value

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str]=Field(
        default=None,
        min_length=5,
        max_length=100,
        description="Updated title (optional, 5-100 characters)"
    )
    content: Optional[str]=Field(
        default= None,
        min_length=10,
        description="Updated content (optional, min 10 characters)"
    )
    tags: Optional[List[str]]=Field(
        default=None,
        description="Updated tags (optional, list of strings)"
    )
    author: Optional[str]=Field(
        default=None,
        max_length=50,
        description="Updated author name (optional, max 50 characters)"
    )
    @field_validator('title', 'content', mode='before')
    @classmethod
    def strip_whitespace(cls, value: Optional[str]):
        if value is not None:
            stripped = value.strip()
            if not stripped:
                raise ValueError("This field cannot be empty or just whitespace")
            return stripped
        return value

class ArticleResponse(ArticleBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class PaginationMeta(BaseModel):
    page: int
    limit: int
    total: int    

class PaginatedArticleResponse(BaseModel):
    items: List[ArticleResponse]
    total: int
    page: int
    limit: int
    total_pages: int
    articles: List[ArticleResponse]
    meta: PaginationMeta

    model_config = ConfigDict(from_attributes=True)