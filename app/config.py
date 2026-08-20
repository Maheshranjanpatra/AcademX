import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-this")

    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = quote_plus(os.environ.get("DB_PASSWORD", ""))
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_NAME = os.environ.get("DB_NAME", "nymora")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

    UPLOAD_FOLDER = os.path.join(os.getcwd(), "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 26 * 1024 * 1024

    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
