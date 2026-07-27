"""
Shared API dependencies.

Authentication
Rate Limiting
Database
Current User
Application Services
"""

import logging
from typing import Generator

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from upstash_ratelimit import Ratelimit, SlidingWindow

from app.auth.security import get_current_user
from app.config.settings import settings
from app.database.postgres import SessionLocal

# ============================
# Services
# ============================

from app.agents.service import multi_agent_service
from app.coach.service import coach_service
from app.goals.service import goals_service
from app.health.service import health_service
from app.market.service import market_service
from app.memory.service import MemoryService
from app.planner.service import planner_service
from app.profile.service import profile_service
from app.recommendations.service import recommendations_service
from app.reports.service import report_service

# =====================================================
# Database Dependency
# =====================================================

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =====================================================
# Redis Client
# =====================================================

from app.cache.redis import redis as cache_redis

# Use the same resilient Redis client as the cache module
redis = cache_redis


# =====================================================
# Rate Limiter
# =====================================================

try:
    ratelimiter = Ratelimit(
        redis=redis,
        limiter=SlidingWindow(20, 60),
        prefix="enterprise-rag",
    )
except Exception as e:
    logging.getLogger(__name__).warning("Failed to initialize Upstash Ratelimit: %s. Rate limiting disabled.", e)

    class DummyRatelimit:
        def limit(self, identifier: str):
            class DummyResponse:
                allowed = True
                reset = 0
            return DummyResponse()

    ratelimiter = DummyRatelimit()


async def rate_limit_dependency(
    request: Request,
    user: dict = Depends(get_current_user),
):
    identifier = user["id"]

    try:
        response = ratelimiter.limit(identifier)

        if not response.allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "message": "Rate limit exceeded.",
                    "retry_after": response.reset,
                },
            )

        return True
    except Exception as e:
        # Log the error but allow the request to proceed if rate limiting fails
        # This prevents the entire application from being unavailable due to rate limiting issues
        logger = logging.getLogger(__name__)
        logger.warning(f"Rate limiting failed, allowing request: {e}")
        return True


# =====================================================
# Authentication
# =====================================================

CurrentUser = Depends(get_current_user)


async def protected_route(
    user=CurrentUser,
    _: bool = Depends(rate_limit_dependency),
):
    return user


# =====================================================
# Service Dependencies
# =====================================================

def get_multi_agent_service():
    return multi_agent_service


def get_profile_service():
    return profile_service


def get_goals_service():
    return goals_service


def get_planner_service():
    return planner_service


def get_market_service():
    return market_service


def get_health_service():
    return health_service


def get_recommendations_service():
    return recommendations_service


def get_memory_service(
    db: Session = Depends(get_db),
):
    return MemoryService(db)


def get_coach_service():
    return coach_service


def get_report_service():
    return report_service