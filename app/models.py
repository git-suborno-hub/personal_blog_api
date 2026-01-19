from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index = True)
    title = Column(String(255), nullable=False, index=True)
    content=Column(Text, nullable=False)
    tags=Column(String(500))
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    is_published=Column(Boolean, default=False, nullable=False)