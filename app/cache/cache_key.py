"""
Cache Key Utilities

Generates deterministic SHA-256 cache keys for:
- Embedding Cache
- RAG Answer Cache
"""

import hashlib


def normalize_text(text: str) -> str:
    """
    Normalize text before hashing.
    """

    return " ".join(
        text.strip().lower().split()
    )


def cache_key(
    prefix: str,
    text: str,
) -> str:
    """
    Generate SHA-256 cache key.

    Example:
        embedding:9d4e1e...
        answer:12ab89...
    """

    normalized = normalize_text(text)

    digest = hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()

    return f"{prefix}:{digest}"


def embedding_key(text: str) -> str:
    """
    Embedding cache key.
    """

    return cache_key(
        "embedding",
        text,
    )


def answer_key(text: str) -> str:
    """
    Answer cache key.
    """

    return cache_key(
        "answer",
        text,
    )


if __name__ == "__main__":

    query = "What is Retrieval Augmented Generation?"

    print(embedding_key(query))

    print(answer_key(query))