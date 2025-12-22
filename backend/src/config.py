try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings  # For older versions
from typing import Optional


class Settings(BaseSettings):
    cohere_api_key: str
    qdrant_url: str
    qdrant_api_key: str
    neon_db_url: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()