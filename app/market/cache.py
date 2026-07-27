"""
Redis cache for market data.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from pydantic import BaseModel

from app.cache.redis import redis

from app.config.settings import settings

logger = logging.getLogger(__name__)


class MarketCache:

    def __init__(self):

        self.redis = redis

        self.ttl = settings.CACHE_TTL

    def _key(
        self,
        category: str,
        identifier: str,
    ) -> str:

        return f"market:{category}:{identifier}"

    def get(
        self,
        category: str,
        identifier: str,
    ) -> dict[str, Any] | None:

        try:

            value = self.redis.get(
                self._key(category, identifier)
            )

            if value is None:
                return None

            if isinstance(value, str):
                return json.loads(value)

            return value

        except Exception:

            logger.exception(
                "Redis GET failed."
            )

            return None

    def set(
        self,
        category: str,
        identifier: str,
        data: BaseModel | dict,
    ) -> None:

        try:

            if isinstance(data, BaseModel):
                payload = data.model_dump()

            else:
                payload = data

            self.redis.set(
                self._key(category, identifier),
                json.dumps(payload, default=str),
                ex=self.ttl,
            )

        except Exception:

            logger.exception(
                "Redis SET failed."
            )

    def delete(
        self,
        category: str,
        identifier: str,
    ) -> None:

        try:

            self.redis.delete(
                self._key(category, identifier)
            )

        except Exception:

            logger.exception(
                "Redis DELETE failed."
            )

    def clear(self) -> None:

        try:

            keys = self.redis.keys("market:*")

            for key in keys:

                self.redis.delete(key)

        except Exception:

            logger.exception(
                "Redis CLEAR failed."
            )