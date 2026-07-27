"""
Redis Cache Layer.
"""

from __future__ import annotations

import json

import redis

from app.config.settings import settings


class MemoryCache:

    def __init__(self):

        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True,
        )

    # =====================================================

    def get(self, key: str):

        value = self.redis.get(key)

        if value is None:
            return None

        return json.loads(value)

    # =====================================================

    def set(
        self,
        key: str,
        value,
        expire: int = 3600,
    ):

        self.redis.set(
            key,
            json.dumps(value),
            ex=expire,
        )

    # =====================================================

    def delete(self, key: str):

        self.redis.delete(key)

    # =====================================================

    def exists(self, key: str):

        return self.redis.exists(key)

    # =====================================================

    def clear(self):

        self.redis.flushdb()


cache = MemoryCache()