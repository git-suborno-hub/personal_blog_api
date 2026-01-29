from app.database import engine
from sqlalchemy import text

def clean_database():
    with engine.connect() as connection:
        connection.execute(text("TRUNCATE TABLE articles RESTART IDENTITY CASCADE;"))
        connection.commit()
        print("Database is fully clean!!")

if __name__ == "__main__":
    clean_database()