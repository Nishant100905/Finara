"""
Application configuration.

All environment variables are loaded from the .env file
and exposed through the `settings` object.

Example:
    from app.core.config import settings

    print(settings.DATABASE_URL)
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------
    APP_NAME: str = "Enterprise Financial Advisor"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------
    DATABASE_URL: str = Field(...)

    # ------------------------------------------------------------------
    # Redis
    # ------------------------------------------------------------------
    REDIS_URL: str = Field(...)

    # ------------------------------------------------------------------
    # Ollama
    # ------------------------------------------------------------------
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "glm-5.2:cloud"

    # ------------------------------------------------------------------
    # Chroma
    # ------------------------------------------------------------------
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000

    # ------------------------------------------------------------------
    # Models
    # ------------------------------------------------------------------
    DEFAULT_LLM: str = "glm-5.2:cloud"
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    # ------------------------------------------------------------------
    # RAG
    # ------------------------------------------------------------------
    TOP_K: int = 10
    RERANK_TOP_K: int = 5

    # ------------------------------------------------------------------
    # Memory
    # ------------------------------------------------------------------
    MAX_CHAT_HISTORY: int = 20
    SUMMARY_TRIGGER: int = 25

    # ------------------------------------------------------------------
    # Cache
    # ------------------------------------------------------------------
    CACHE_TTL: int = 3600

    # ------------------------------------------------------------------
    # Timeouts
    # ------------------------------------------------------------------
    REQUEST_TIMEOUT: int = 30

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    LOG_LEVEL: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()


settings = get_settings()

LANGCHAIN_TRACING_V2: bool = False

LANGCHAIN_API_KEY: str = ""

LANGCHAIN_PROJECT: str = "Enterprise-RAG"

LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"

SESSION_TTL: int = 86400

MAX_FILE_SIZE: int = 10485760

ENVIRONMENT: str = "development"

ALLOWED_ORIGINS: list[str] = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
DATABASE_SSLMODE: str = "require"
