import os
import sys

# app ফোল্ডারকে Python path-এ যোগ করা (যদি script টা root থেকে চালানো হয়)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# এখন relative import করা যাবে
from app.database import engine, Base
from app import models  # models.py লোড হবে যাতে সব class register হয়

print("Creating tables if they don't exist...")
Base.metadata.create_all(bind=engine)
print("Done! Tables created successfully (or already existed).")