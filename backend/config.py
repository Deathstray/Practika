from pathlib import Path
import os

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
SQLITE_DIR = BASE_DIR / "data"
SQLITE_DIR.mkdir(parents=True, exist_ok=True)


def _default_database_url() -> str:
    return f"sqlite:///{(SQLITE_DIR / 'transport_db.sqlite3').as_posix()}"


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", _default_database_url())
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-jwt-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "127.0.0.1")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8001"))

    class Config:
        env_file = ".env"


settings = Settings()
