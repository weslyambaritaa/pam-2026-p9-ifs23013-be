import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_PORT = os.getenv("APP_PORT")
    # Ubah bagian ini:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
    
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False