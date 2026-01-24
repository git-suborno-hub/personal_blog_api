import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()  # .env ফাইল থেকে ভেরিয়েবল লোড

# Database URL .env থেকে নেওয়া
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL .env ফাইলে পাওয়া যায়নি। দয়া করে চেক করুন।")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,               # True করলে SQL query দেখা যাবে (development-এ সুবিধা)
    pool_pre_ping=True,       # connection চেক করে stale connection এড়ায়
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
