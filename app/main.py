from fastapi import FastAPI
from app.routes import articles

app=FastAPI()

@app.get("/")

@app.get("/health")
def health_check():
    return {"status":"ok"}

app.include_router(articles.router)