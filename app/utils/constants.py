"""
Application Constants
"""

# ==========================================================
# Application
# ==========================================================

APP_NAME = "Enterprise RAG System"

API_VERSION = "v1"

DEFAULT_TOP_K = 10

MAX_TOP_K = 20

DEFAULT_TEMPERATURE = 0.2

MAX_QUERY_LENGTH = 5000

DEFAULT_CACHE_TTL = 3600

# ==========================================================
# Models
# ==========================================================

OLLAMA_MODEL = "glm-5.2:cloud"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

RERANKER_MODEL = "BAAI/bge-reranker-base"

# ==========================================================
# Retrieval
# ==========================================================

RRF_K = 60

CRAG_THRESHOLD = 0.70

SELF_RAG_THRESHOLD = 0.70

MAX_RETRIEVAL_RESULTS = 10

MAX_WEB_RESULTS = 5

# ==========================================================
# ChromaDB
# ==========================================================

COLLECTION_NAME = "enterprise_rag"

# ==========================================================
# Redis
# ==========================================================

ANSWER_CACHE_PREFIX = "answer"

EMBEDDING_CACHE_PREFIX = "embedding"

# ==========================================================
# Logging
# ==========================================================

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

LOG_LEVEL = "INFO"

# ==========================================================
# Security
# ==========================================================

MAX_INPUT_LENGTH = 5000

MIN_PASSWORD_LENGTH = 8

REQUEST_TIMEOUT = 30
