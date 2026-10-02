import os
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
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-this")

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
    # Google OAuth
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

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
