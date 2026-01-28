import os
from pathlib import Path
from dotenv import load_dotenv

# set the .env file location
env_path=Path(__file__).resolve().parent.parent / ".env"

# load data from .env file
load_dotenv(dotenv_path=env_path)

class Settings:
    # database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # app configuration
    APP_NAME : str = "My Professional Blog API"
    DEBUG: bool = os.getenv("DEBUG_MODE", "False") == "True"
    PORT: int = int(os.getenv("APP_PORT", 8000))
    
settings=Settings()