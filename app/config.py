import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-this")

    # PostgreSQL Database URL
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google OAuth
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

    # Uploads
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 26 * 1024 * 1024 #26 MB

    # YouTube API
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
