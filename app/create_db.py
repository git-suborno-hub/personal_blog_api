import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.database import engine, Base
from app import models  

print("Creating tables if they don't exist...")
Base.metadata.create_all(bind=engine)
print("Done! Tables created successfully (or already existed).")