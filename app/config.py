import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

def _normalize_db_url(url: str | None) -> str | None:
    if not url:
        return url
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://") and "+psycopg" not in url:
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "true").lower() == "true"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    # PostgreSQL Database URL
    SQLALCHEMY_DATABASE_URI = _normalize_db_url(os.environ.get("DATABASE_URL"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Recycle connections before Neon suspends them + pre-ping dead ones
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
        "connect_args": {
            "connect_timeout": 15,
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 3,
        },
    }
    # Uploads
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 26 * 1024 * 1024 #26 MB

    # YouTube API
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

    # Backblaze B2
    B2_KEY_ID = os.environ.get("B2_KEY_ID")
    B2_APPLICATION_KEY = os.environ.get("B2_APPLICATION_KEY")
    B2_BUCKET_NAME = os.environ.get("B2_BUCKET_NAME")
    B2_ENDPOINT = os.environ.get("B2_ENDPOINT")
    B2_REGION = "us-west-004"
