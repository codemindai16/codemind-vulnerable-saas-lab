from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://codemind:codemind@db:5432/codemind"
    SECRET_KEY: str = "weak-secret-key-123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 999999
    UPLOAD_DIR: str = "/app/uploads"
    MAX_UPLOAD_SIZE: int = 10485760
    REDIS_URL: str = "redis://redis:6379/0"
    WEBHOOK_TIMEOUT: int = 10

    class Config:
        env_file = ".env"

settings = Settings()
