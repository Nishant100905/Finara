"""
RAG Answer Cache

Caches complete RAG responses for 1 hour.
"""

import json
import logging
from typing import Optional

from app.cache.cache_key import answer_key
from app.cache.redis import redis

logger = logging.getLogger(__name__)

# 1 Hour TTL
ANSWER_CACHE_TTL = 60 * 60


class AnswerCache:
    """
    Cache final LLM answers.
    """

    def __init__(self):
        self.redis = redis

    # --------------------------------------------------

    def get(
        self,
        query: str,
    ) -> Optional[str]:

        key = answer_key(query)

        try:
            cached = self.redis.get(key)
        except Exception as e:
            # Fail open: a cache outage should not 500 the chat.
            # Treat as a miss and let the LLM answer.
            logger.warning(
                "Answer cache lookup failed, falling back to LLM: %s",
                e,
            )
            return None

        if cached is None:

            logger.info(
                f"Answer Cache MISS: {key}"
            )

            return None

        logger.info(
            f"Answer Cache HIT: {key}"
        )

        if isinstance(cached, bytes):
            cached = cached.decode()

        data = json.loads(cached)

        return data["answer"]

    # --------------------------------------------------

    def set(
        self,
        query: str,
        answer: str,
    ):

        key = answer_key(query)

        payload = {
            "query": query,
            "answer": answer,
        }

        try:
            self.redis.set(
                key,
                json.dumps(payload),
                ex=ANSWER_CACHE_TTL,
            )
        except Exception as e:
            # Cache writes are best-effort. Log and move on so the
            # user's answer is still returned.
            logger.warning(
                "Answer cache write failed, continuing without cache: %s",
                e,
            )
            return

        logger.info(
            f"Answer Cached: {key}"
        )

    # --------------------------------------------------

    def delete(
        self,
        query: str,
    ):

        key = answer_key(query)

        self.redis.delete(key)

    # --------------------------------------------------

    def exists(
        self,
        query: str,
    ) -> bool:

        key = answer_key(query)

        return self.redis.exists(key)

    # --------------------------------------------------

    def refresh(
        self,
        query: str,
    ):

        key = answer_key(query)

        self.redis.expire(
            key,
            ANSWER_CACHE_TTL,
        )

    # --------------------------------------------------

    def clear(self):

        """
        WARNING:
        Deletes all cache entries.
        Use only during development.
        """

        cursor = 0

        while True:

            cursor, keys = self.redis.scan(
                cursor=cursor,
                match="answer:*",
            )

            if keys:
                self.redis.delete(*keys)

            if cursor == 0:
                break


# ==========================================================
# Singleton
# ==========================================================

answer_cache = AnswerCache()


# ==========================================================
# Helper Functions
# ==========================================================

def get_cached_answer(
    query: str,
):

    return answer_cache.get(query)


def cache_answer(
    query: str,
    answer: str,
):

    answer_cache.set(
        query,
        answer,
    )


def invalidate_answer(
    query: str,
):

    answer_cache.delete(query)