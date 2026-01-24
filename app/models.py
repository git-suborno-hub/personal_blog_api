from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from .database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String, default="Anonymous")
    tags = Column(String)                       # পরে চাইলে এটাকে JSON বা relationship-এ পরিবর্তন করা যাবে
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)