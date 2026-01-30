import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.logger import logger 

load_dotenv()  


DATABASE_URL = os.getenv("DATABASE_URL")
logger.info(f"Using DATABASE_URL from env: {DATABASE_URL}")

if not DATABASE_URL:
    logger.error("No DATABASE_URL found! Falling back or raising error.")
    raise ValueError("DATABASE_URL environment variable is required!")

engine = create_engine(
    DATABASE_URL,
    echo=True,                  
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
