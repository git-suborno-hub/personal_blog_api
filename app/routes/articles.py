from fastapi import APIRouter
from datetime import datetime

router=APIRouter(prefix="/articles", tags=["Articles"])

fake_articles = [
    {
        "id":1,
        "title" : "First Article",
        "content": "This is my first blog post",
        "tags" : ["intro"],
        "created_at" : datetime.utcnow()
    }
]

@router.get("/")
def get_articles():
    return fake_articles