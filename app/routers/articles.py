from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.models import Article
from app.schemas.article import ArticleResponse, ArticleCreate, PaginatedArticleResponse, ArticleUpdate
from app.schemas.response import BaseResponse, MessageResponse, ErrorResponse

router = APIRouter()


# POST endpoint - Create a new article
@router.post(
    "/",
    response_model=BaseResponse[ArticleResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new article"
)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    try:
        tags_str = None
        if isinstance(article.tags, list):
            tags_str = ", ".join(article.tags)
        elif isinstance(article.tags, str):
            tags_str = article.tags.strip()

        db_article = Article(
            title=article.title,
            content=article.content,
            tags=tags_str,
            author=article.author if article.author else "Anonymous"
        )

        db.add(db_article)
        db.commit()
        db.refresh(db_article)

        return {
            "success": True,
            "data": {
                "id": db_article.id,
                "title": db_article.title,
                "content": db_article.content,
                "author": db_article.author,
                "tags": db_article.tags,
                "created_at": db_article.created_at.isoformat() if db_article.created_at else None
            }
        }
    
    except Exception as e:
        print(f"POST article error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Something went wrong on our end. Please try again later."}
        )    


# GET all articles - with pagination and tag filter
@router.get(
    "/",
    response_model=BaseResponse[PaginatedArticleResponse],
    summary="Get articles with page-based pagination and tag filter"
)
def get_articles(
    db: Session = Depends(get_db),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Items per page (1-100)")
):
    try:
        query = db.query(Article)
        
        if tag:
            query = query.filter(Article.tags.ilike(f"%{tag}%"))
        
        total = query.count()  

        skip = (page - 1) * limit  

        articles = query.offset(skip).limit(limit).all()

        paginated = {
            "items": [
                {
                    "id": a.id,
                    "title": a.title,
                    "content": a.content,
                    "author": a.author,
                    "tags": a.tags,
                    "created_at": a.created_at.isoformat() if a.created_at else None
                }
                for a in articles
            ],
            "meta":{
                "page": page,
                "limit": limit,
                "total": total,
            }
        }
        
        total_pages = (total + limit - 1) // limit if limit > 0 else 1
        paginated["total_pages"] = total_pages

        return BaseResponse[PaginatedArticleResponse](
            success=True,
            data=paginated
        )

    except Exception as e:
        print(f"GET articles error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Unable to fetch articles. Try again later."}
        )


# GET single article by ID
@router.get(
    "/{id}",
    response_model=BaseResponse[ArticleResponse],
    responses={404: {"model": ErrorResponse}},
    summary="Get a single article by ID"
)
def get_article(id: int, db: Session = Depends(get_db)):
    try: 
        article = db.query(Article).filter(Article.id == id).first()
        if not article:
            raise HTTPException(
                status_code=404,
                detail={"success": False, "error": "Article not found"}
            )

        return {
            "success": True,
            "data": {
                "id": article.id,
                "title": article.title,
                "content": article.content,
                "author": article.author,
                "tags": article.tags,
                "created_at": article.created_at.isoformat() if article.created_at else None
            }
        }
        
    except Exception as e:
        print(f"GET article {id} error: {str(e)}")
        raise HTTPException(
            status_code=404,
            detail={"success": False, "error": "Article not found."}
        )   
    


# PUT endpoint - Update an existing article
@router.put(
    "/{id}",
    response_model=BaseResponse[ArticleResponse],
    summary="Update an existing article",
    description="Partially updates the title, content, tags, and author of an article by its ID."
)
def update_article(
    id: int,
    article_update: ArticleUpdate,
    db: Session = Depends(get_db)
):
    db_article = db.query(Article).filter(Article.id == id).first()

    if not db_article:
        raise HTTPException(
            status_code=404,
            detail={"success": False, "error": "Article not found"}
        )

    # শুধু পাঠানো ফিল্ডগুলো
    update_data = article_update.model_dump(exclude_unset=True)

    # Empty update চেক
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "error": "At least one field must be provided for update"
            }
        )

    # আপডেট করা
    for key, value in update_data.items():
        setattr(db_article, key, value)

    try:
        db.commit()
        db.refresh(db_article)
    except Exception as e:
        # শুধু ডাটাবেস/অন্যান্য unexpected error ধরবে
        # 400/404 ইত্যাদি এখানে আসবে না
        print(f"PUT /articles/{id} error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Something went wrong while updating the article. Please try again later."}
        )

    return {
        "data": {
            "id": db_article.id,
            "title": db_article.title,
            "content": db_article.content,
            "author": db_article.author,
            "tags": db_article.tags,
            "created_at": db_article.created_at.isoformat() if db_article.created_at else None
        }
    }


# DELETE endpoint - Delete an article
@router.delete(
    "/{id}",
    response_model=MessageResponse,
    summary="Delete an article",
    description="Deletes a specific article by its ID from the database."
)
def delete_article(
    id: int,
    db: Session = Depends(get_db)
):
    try:
        article = db.query(Article).filter(Article.id == id).first()

        if not article:
            raise HTTPException(
                status_code=404,
                detail={"success": False, "error": "Article not found"}
            )

        db.delete(article)
        db.commit()

        return MessageResponse(success=True, message="Article deleted successfully")
    
    except Exception as e:
        print(f"DELETE /articles/{id} error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "Something went wrong while deleting the article. Please try again later."
            }
        )