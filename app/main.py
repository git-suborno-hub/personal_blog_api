from fastapi import FastAPI, Depends
from .database import get_db
from sqlalchemy.orm import Session
from . import models
from .database import engine

app=FastAPI(title="personal blog api")

@app.get("/")
def root():
    return {"message":"welcome to personal blog api"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "Database connection successfully!"}

models.Base.metadata.create_all(bind=engine)