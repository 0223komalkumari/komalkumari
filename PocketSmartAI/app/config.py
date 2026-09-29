from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

class Settings:
    app_name = os.getenv("APP_NAME", "PocketSmart AI")
    app_env = os.getenv("APP_ENV", "development")
    secret_key = os.getenv("SECRET_KEY", "dev-only-change-me")
    gemini_api_key = os.getenv("GEMINI_API_KEY", "")
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    database_path = os.getenv("DATABASE_PATH", str(DATA_DIR / "pocketsmart.db"))
    max_image_mb = int(os.getenv("MAX_IMAGE_MB", "5"))
    access_token_minutes = int(os.getenv("ACCESS_TOKEN_MINUTES", "60"))
    allowed_origins = [x.strip() for x in os.getenv(
        "ALLOWED_ORIGINS", "http://127.0.0.1:8000,http://localhost:8000"
    ).split(",") if x.strip()]

settings = Settings()
