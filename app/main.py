from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models
from .routers import articles
# from .database import get_db

app = FastAPI(
    title="Personal Blog API",
    description="আমার ব্যক্তিগত ব্লগের backend",
    version="0.1.0"
)

# প্রথমবার চালালে টেবিল তৈরি হবে (development-এ রাখা ভালো)
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Personal Blog API চলছে! Docs দেখতে /docs যাও"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(articles.router)