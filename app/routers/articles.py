from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Article
from app.schemas.article import ArticleResponse, ArticleCreate

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description":"Not Found"}},
)

# POST endpoint
@router.post(
    "/",
    response_model=ArticleResponse,
    status_code= 201,
    summary="Create a new article"
)

def create_article(article: ArticleCreate, db: Session=Depends(get_db)):
    db_article=Article(
        title=article.title,
        content=article.content,
        tags=", ".join(article.tags) if article.tags else None,
        author="Anonymous"
    )

    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

# GET endpoint
@router.get(
    "/",
    response_model=List[ArticleResponse],
    summary="Get all articles",
    description="Returns a list of all blog articles from the databse."
)

def get_all_articles(db: Session=Depends(get_db)):
    articles=db.query(Article).all()
    return articles