from fastapi import FastAPI
from app.routers import articles

app = FastAPI(
    title="Personal Blog API",
    description="A simple blog API with CRUD operations",
    version="1.0.0"
)

app.include_router(
    articles.router,
    prefix="/api/v1/articles",   
    tags=["articles"]            
)