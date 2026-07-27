"""
Embedding Cache

Stores embeddings in Upstash Redis for 7 days.
"""

import json
import logging
from typing import List

from langchain_core.embeddings import Embeddings

from app.cache.cache_key import embedding_key
from app.cache.redis import redis

logger = logging.getLogger(__name__)

EMBEDDING_CACHE_TTL = 60 * 60 * 24 * 7  # 7 Days


class EmbeddingCache:

    def __init__(
        self,
        embedding_model: Embeddings,
    ):
        self.embedding_model = embedding_model

    # --------------------------------------------------

    def get_embedding(
        self,
        text: str,
    ) -> List[float]:

        key = embedding_key(text)

        cached = redis.get(key)

        if cached is not None:

            logger.info(f"Embedding Cache HIT: {key}")

            if isinstance(cached, bytes):
                cached = cached.decode()

            return json.loads(cached)

        logger.info(f"Embedding Cache MISS: {key}")

        embedding = self.embedding_model.embed_query(text)

        redis.set(
            key,
            json.dumps(embedding),
            ex=EMBEDDING_CACHE_TTL,
        )

        return embedding

    # --------------------------------------------------

    def delete_embedding(
        self,
        text: str,
    ):

        redis.delete(
            embedding_key(text)
        )

    # --------------------------------------------------

    def exists(
        self,
        text: str,
    ) -> bool:

        return bool(
            redis.exists(
                embedding_key(text)
            )
        )

    # --------------------------------------------------

    def cache_size(
        self,
        text: str,
    ) -> int:

        value = redis.get(
            embedding_key(text)
        )

        if value is None:
            return 0

        if isinstance(value, bytes):
            value = value.decode()

        return len(value)

    # --------------------------------------------------

    def refresh(
        self,
        text: str,
    ):

        redis.expire(
            embedding_key(text),
            EMBEDDING_CACHE_TTL,
        )