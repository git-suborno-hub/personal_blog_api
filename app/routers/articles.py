from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import Article
from app.schemas.article import ArticleResponse, ArticleCreate, PaginatedArticleResponse

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
    tags_str = None
    if isinstance(article.tags, list):
        tags_str=", ".join(article.tags)
    elif isinstance(article.tags, str):
        tags_str=article.tags.strip()

        
    db_article=Article(
        title=article.title,
        content=article.content,
        tags=tags_str,
        author=article.author if article.author else "Anonymous"
    )

    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

# GET endpoint
@router.get(
    "/",
    response_model=PaginatedArticleResponse,
    summary="Get paginated articles with total count + optional tag filters",
    description="Returns a paginated list of articles along with the total count."
)

def get_articles(
    db: Session = Depends(get_db),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    query = db.query(Article)
    
    print(f"Received tag: '{tag}'")  # ← এটা দেখাবে tag আসলেই আসছে কি না
    
    if tag:
        print(f"Applying filter for tag: {tag}")
        query = query.filter(Article.tags.ilike(f"%{tag}%"))
        print(f"SQL after filter: {str(query)}")  # ← generated SQL দেখাবে
    
    total = query.count()
    articles = query.offset(offset).limit(limit).all()
    
    return {
        "items": articles,
        "total": total,
        "limit": limit,
        "offset": offset
    }


# GET/articles/{id} endpoint

@router.get(
    "/{id}",
    response_model=ArticleResponse
)

def get_article(
    id: int,
    db: Session=Depends(get_db)
):
    article=db.query(Article).filter(Article.id==id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return article

# PUT endpoint
@router.put(
    "/{id}",
    response_model=ArticleResponse,
    summary="Update an existing article",
    description="Updates the title, content, and tags of an article by its ID."
)
def update_article(
    id: int,
    article_update: ArticleCreate,
    db: Session = Depends(get_db)
):
    
    db_article = db.query(Article).filter(Article.id == id).first()
    
    
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    
    db_article.title = article_update.title
    db_article.content = article_update.content
    
    
    if article_update.tags:
        db_article.tags = ", ".join(article_update.tags)
    else:
        db_article.tags = None
    
    db.commit()
    db.refresh(db_article)
    
    return db_article


# DELETE endpoint
@router.delete(
    "/{id}",
    status_code=200,
    summary="Delete an article",
    description="Deletes a specific article by its ID from the database."
)

def delete_article(
    id:int,
    db: Session=Depends(get_db)
):
    article=db.query(Article).filter(Article.id==id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found.")
    
    db.delete(article)
    db.commit()

    return {"message": "Successfully deleted."}