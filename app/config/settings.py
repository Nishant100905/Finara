"""
Application Settings
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from .env
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ==========================================================
    # Application
    # ==========================================================

    APP_NAME: str = "Enterprise RAG System"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = False

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    # ==========================================================
    # Security
    # ==========================================================

    SECRET_KEY: str = Field(...)

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ==========================================================
    # Ollama
    # ==========================================================

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    OLLAMA_MODEL: str = "glm-5.2:cloud"

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    # ==========================================================
    # Supabase
    # ==========================================================

    SUPABASE_URL: str = Field(...)

    SUPABASE_ANON_KEY: str = Field(...)

    SUPABASE_SERVICE_ROLE_KEY: str = Field(...)

    SUPABASE_JWKS_URL: str = Field(...)

    DATABASE_SSLMODE: str = "require"
    # ==========================================================
    # PostgreSQL
    # ==========================================================

    DATABASE_URL: str = Field(...)

    # ==========================================================
    # ChromaDB
    # ==========================================================

    CHROMA_DB_PATH: str = "./chroma_db"

    CHROMA_COLLECTION: str = "enterprise_rag"

    # ==========================================================
    # Redis (Upstash)
    # ==========================================================

    UPSTASH_REDIS_REST_URL: str = Field(...)

    UPSTASH_REDIS_REST_TOKEN: str = Field(...)

    CACHE_TTL: int = 3600

    # ==========================================================
    # Tavily
    # ==========================================================

    TAVILY_API_KEY: str = Field(...)

    # ==========================================================
    # Retrieval
    # ==========================================================

    TOP_K: int = 10

    RRF_K: int = 60

    # Threshold (0..1) used by the deterministic relevance
    # check. A chunk set is considered RELEVANT when its
    # top-score (max of dense cosine similarity and
    # cross-encoder sigmoid) is >= this value.
    #
    # 0.70 is a robust threshold: high confidence RAG chunks answer
    # directly, while weak/unrelated retrieval triggers Tavily web search.
    RAG_RELEVANCE_THRESHOLD: float = 0.70

    # Backward-compatible alias used by older code paths.
    CRAG_THRESHOLD: float = 0.70

    SELF_RAG_THRESHOLD: float = 0.70

    MAX_WEB_RESULTS: int = 5

    # ==========================================================
    # Logging
    # ==========================================================

    LOG_LEVEL: str = "INFO"

    # ==========================================================
    # CORS
    # ==========================================================

    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]


@lru_cache
def get_settings() -> Settings:
    """
    Returns cached application settings.
    """
    return Settings()


settings = get_settings()

settings = get_settings()

print("\n" + "=" * 70)
print("DATABASE_URL loaded by Settings:")
print(settings.DATABASE_URL)
print("=" * 70 + "\n")

print("=" * 60)
print("SUPABASE_URL:", settings.SUPABASE_URL)
print("SUPABASE_ANON_KEY:", settings.SUPABASE_ANON_KEY[:30] if settings.SUPABASE_ANON_KEY else "EMPTY")
print("=" * 60)