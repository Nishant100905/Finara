"""
Upstash Redis Client
"""

import logging
from typing import Optional

from upstash_redis import Redis
from upstash_redis.errors import UpstashError as RedisError

from app.config.settings import settings


logger = logging.getLogger(__name__)


class RedisClient:
    """
    Singleton Redis Client with graceful degradation
    """

    _client: Redis | None = None
    _available: bool = True

    @classmethod
    def get_client(cls) -> Redis:

        if cls._client is None and cls._available:
            try:
                cls._client = Redis(
                    url=settings.UPSTASH_REDIS_REST_URL,
                    token=settings.UPSTASH_REDIS_REST_TOKEN,
                )
                # Test the connection
                cls._client.ping()
                logger.info("Connected to Upstash Redis successfully")
            except Exception as e:
                logger.warning(f"Failed to connect to Upstash Redis: {e}")
                cls._available = False
                # Return a mock client that will fail gracefully
                return cls._get_fallback_client()

        return cls._client

    @classmethod
    def _get_fallback_client(cls) -> Redis:
        """
        Returns a fallback client that handles errors gracefully
        """
        class FallbackRedis:
            def __init__(self):
                self._headers = {}

            def __getattr__(self, name):
                # Return a method that logs and returns appropriate default values
                def fallback_method(*args, **kwargs):
                    logging.warning(f"Redis operation '{name}' failed due to unavailable connection")
                    # Return appropriate defaults based on common Redis method return types
                    if name in ['get', 'execute']:  # Commands that typically return values
                        return None
                    elif name in ['exists', 'ping']:  # Commands that return boolean
                        return False
                    elif name in ['delete', 'set', 'expire']:  # Commands that return count
                        return 0
                    else:
                        return None
                return fallback_method

        return FallbackRedis()


redis = RedisClient.get_client()


def ping() -> bool:
    """
    Check Redis connectivity.
    """

    if not RedisClient._available:
        return False

    try:
        redis.set("ping", "pong", ex=5)

        return redis.get("ping") == "pong"

    except Exception as e:
        logger.warning(f"Redis ping failed: {e}")
        RedisClient._available = False
        return False