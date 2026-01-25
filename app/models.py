from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from .database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)          # index যোগ করা যায় search-এর জন্য
    content = Column(Text, nullable=False)
    # author = Column(String, default="Anonymous", index=True)    # author-এও index দিলে ভালো
    author = Column(String, index=True)    # author-এও index দিলে ভালো
    tags = Column(String, nullable=True)                        # nullable=True রাখা ভালো (কোনো tag না থাকলে None হবে)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)  # sorting-এর জন্য index

    # Optional: __repr__ যোগ করলে debug-এ সুবিধা হয়
    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title}', tags='{self.tags}')>"