from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.models import Article
from app.schemas.article import ArticleResponse, ArticleCreate, PaginatedArticleResponse, ArticleUpdate
from app.schemas.response import BaseResponse, MessageResponse, ErrorResponse
from app.logger import logger 

router = APIRouter()


# POST endpoint - Create a new article
@router.post(
    "/",
    response_model=BaseResponse[ArticleResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new article",
    description="To create an article, you need a title and content. Remember, the title must be unique.",
    responses={  # ← এই responses প্যারামিটার যোগ করো
        201: {
            "description": "Article successfully created",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "id": 1,
                            "title": "FastAPI দিয়ে ২০২৫ সালে API বানানোর সেরা প্র্যাকটিস",
                            "content": "এই আর্টিকেলে আমরা FastAPI-এর সাথে ...",
                            "author": "Suborno",
                            "tags": ["fastapi", "python"],
                            "created_at": "2025-01-01T12:00:00"
                        }
                    }
                }
            }
        },
        400: {
            "description": "Validation error (e.g. title too short)",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "string_too_short",
                                "loc": ["body", "title"],
                                "msg": "String should have at least 5 characters",
                                "input": "Hi"
                            }
                        ]
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": "Something went wrong on our end. Please try again later."
                    }
                }
            }
        }
    }
)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    
    # Log incoming request details
    logger.info(f"Incoming POST /articles - Title: '{article.title}', Author: '{article.author or 'Anonymous'}'")

    try:
        # Prepare tags as comma-separated string
        tags_str = None
        if isinstance(article.tags, list):
            tags_str = ", ".join(article.tags)
        elif isinstance(article.tags, str):
            tags_str = article.tags.strip()

        # Create new Article instance
        db_article = Article(
            title=article.title,
            content=article.content,
            tags=tags_str,
            author=article.author if article.author else "Anonymous"
        )

        # Save to database
        db.add(db_article)
        db.commit()
        db.refresh(db_article)

        # Log success
        logger.info(f"Success: Article created - ID: {db_article.id}, Title: '{db_article.title}'")

        # Return formatted response
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
        # Log error and return clean 500 response
        logger.error(f"Failure: POST /articles failed - Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Something went wrong on our end. Please try again later."}
        )


# GET all articles - with page-based pagination and tag filter
@router.get(
    "/",
    response_model=BaseResponse[PaginatedArticleResponse],
    summary="List all articles",
    description="You can view a list of all articles using pagination and tag filters. The default is page 1 and the limit is 10.",
    responses={  # ← এখানে responses যোগ করো
        200: {
            "description": "List of articles with pagination metadata",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "items": [
                                {
                                    "id": 1,
                                    "title": "Sample Article",
                                    "content": "Sample content...",
                                    "author": "Suborno",
                                    "tags": ["python"],
                                    "created_at": "2025-01-01T12:00:00"
                                }
                            ],
                            "meta": {
                                "page": 1,
                                "limit": 10,
                                "total": 47
                            }
                        }
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": "Unable to fetch articles. Try again later."
                    }
                }
            }
        }
    }
)
def get_articles(
    db: Session = Depends(get_db),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Items per page (1-100)")
):
    
    # Log incoming request with query params
    logger.info(f"Incoming GET /articles?page={page}&limit={limit}&tag={tag}")

    try:
        # Build base query
        query = db.query(Article)

        # Apply tag filter if provided
        if tag:
            query = query.filter(Article.tags.ilike(f"%{tag}%"))

        # Get total count (before pagination)
        total = query.count()

        # Calculate skip/offset based on page
        skip = (page - 1) * limit

        # Fetch paginated articles
        articles = query.offset(skip).limit(limit).all()

        # Prepare response data
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
            "meta": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": (total + limit - 1) // limit if limit > 0 else 1
            }
        }

        # Log success with number of items fetched
        logger.info(f"Success: Fetched {len(articles)} articles on page {page} (total: {total})")

        return {
            "success": True,
            "data": paginated
        }

    except Exception as e:
        # Log error and return clean 500 response
        logger.error(f"Failure: GET /articles failed - Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Unable to fetch articles. Try again later."}
        )


# GET single article by ID
@router.get(
    "/{id}",
    response_model=BaseResponse[ArticleResponse],
    summary="Get article details",
    description="Detailed information about a specific article can be found through the ID. If the ID is not found, a 4-0-4 error will be returned.",
    responses={
        200: {
            "description": "Article found",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "id": 1,
                            "title": "Sample",
                            "content": "...",
                            "author": "Suborno",
                            "tags": ["python"],
                            "created_at": "2025-01-01T12:00:00"
                        }
                    }
                }
            }
        },
        404: {
            "description": "Article not found",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": "Article not found"
                    }
                }
            }
        }
    }
)
def get_article(id: int, db: Session = Depends(get_db)):
    
    # Log incoming request
    logger.info(f"Incoming GET /articles/{id}")

    try:
        article = db.query(Article).filter(Article.id == id).first()

        if not article:
            # Log warning for not found
            logger.warning(f"Failure: Article not found - ID: {id}")
            raise HTTPException(
                status_code=404,
                detail={"success": False, "error": "Article not found"}
            )

        # Log success
        logger.info(f"Success: Fetched article - ID: {id}, Title: '{article.title}'")

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
        # Log unexpected error
        logger.error(f"Failure: GET /articles/{id} failed - Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Something went wrong. Please try again later."}
        )


# PUT endpoint - Update an existing article
@router.put(
    "/{id}",
    response_model=BaseResponse[ArticleResponse],
    summary="Update an article",
    description=(
        "Update a specific article by ID. "
        "You can do a partial update if you want—that is, just send the title or just the content. "
        "If you don't send any fields, they will remain as they were."
    ),
    responses={  # ← এই responses যোগ করো
        200: {
            "description": "Article successfully updated",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "id": 33,
                            "title": "FastAPI দিয়ে ২০২৫ সালে API বানানোর সেরা প্র্যাকটিস (Updated)",
                            "content": "এই আর্টিকেলে আমরা FastAPI-এর সাথে ... (Updated content)",
                            "author": "Suborno",
                            "tags": ["fastapi", "python", "api"],
                            "created_at": "2026-01-25T11:29:39.161433"
                        }
                    }
                }
            }
        },
        400: {
            "description": "Bad request (e.g. empty update or invalid data)",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": "At least one field must be provided for update"
                    }
                }
            }
        },
        404: {
            "description": "Article not found",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": "Article not found"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": "Something went wrong while updating the article. Please try again later."
                    }
                }
            }
        }
    }
)
def update_article(
    id: int,
    article_update: ArticleUpdate,
    db: Session = Depends(get_db)
):
    
    # Log incoming request with updated fields
    updated_fields = list(article_update.model_dump(exclude_unset=True).keys())
    logger.info(f"Incoming PUT /articles/{id} - Updating fields: {updated_fields}")

    db_article = db.query(Article).filter(Article.id == id).first()

    if not db_article:
        logger.warning(f"Failure: Article not found - ID: {id}")
        raise HTTPException(
            status_code=404,
            detail={"success": False, "error": "Article not found"}
        )

    # Get only the fields that were provided
    update_data = article_update.model_dump(exclude_unset=True)

    # Check for empty update
    if not update_data:
        logger.warning(f"Failure: Empty update attempt - ID: {id}")
        raise HTTPException(
            status_code=400,
            detail={"success": False, "error": "At least one field must be provided for update"}
        )

    # Apply updates
    for key, value in update_data.items():
        setattr(db_article, key, value)

    try:
        db.commit()
        db.refresh(db_article)

        # Log success
        logger.info(f"Success: Updated article - ID: {id}")

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
        logger.error(f"Failure: PUT /articles/{id} failed - Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Something went wrong while updating the article. Please try again later."}
        )


# DELETE endpoint - Delete an article
@router.delete(
    "/{id}",
    response_model=MessageResponse,
    summary="Delete an article",
    description=(
        "Permanently delete an article from the database by ID."
        "Remember, once deleted, this data cannot be recovered."
    ),
    responses={  # ← এই responses যোগ করো
        200: {
            "description": "Article successfully deleted",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Article deleted successfully"
                    }
                }
            }
        },
        404: {
            "description": "Article not found",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": "Article not found"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": "Something went wrong while deleting the article. Please try again later."
                    }
                }
            }
        }
    }
)
def delete_article(
    id: int,
    db: Session = Depends(get_db)
):
    
    # Log incoming request
    logger.info(f"Incoming DELETE /articles/{id}")

    try:
        article = db.query(Article).filter(Article.id == id).first()

        if not article:
            logger.warning(f"Failure: Article not found - ID: {id}")
            raise HTTPException(
                status_code=404,
                detail={"success": False, "error": "Article not found"}
            )

        db.delete(article)
        db.commit()

        # Log success
        logger.info(f"Success: Deleted article - ID: {id}")

        return MessageResponse(success=True, message="Article deleted successfully")

    except Exception as e:
        logger.error(f"Failure: DELETE /articles/{id} failed - Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Something went wrong while deleting the article. Please try again later."}
        )