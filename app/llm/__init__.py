from .embeddings import embeddings
from .factory import create_llm
from .ollama import get_llm
from .prompts import (
    FINANCIAL_PROMPT,
    SYSTEM_PROMPT,
)

__all__ = [
    "llm",
    "embeddings",
    "create_llm",
    "SYSTEM_PROMPT",
    "FINANCIAL_PROMPT",
]

llm = get_llm()
