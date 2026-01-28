from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from .database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)          
    content = Column(Text, nullable=False)
    author = Column(String, index=True)    
    tags = Column(String, nullable=True)                        
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)  

    
    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title}', tags='{self.tags}')>"