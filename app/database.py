# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file name (এটা তোমার প্রজেক্ট ফোল্ডারের ভিতরে তৈরি হবে)
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# SQLite-এর জন্য extra argument দরকার (multi-threaded FastAPI-এর জন্য)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}   # এটা না দিলে error আসতে পারে
)

# SessionLocal হচ্ছে factory — প্রতিবার নতুন session বানাবে
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class — পরে models এটা inherit করবে
Base = declarative_base()

# Dependency function (FastAPI routes-এ db পাঠানোর জন্য)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()