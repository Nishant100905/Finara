"""
Health Check API
"""

import platform
from datetime import datetime

from fastapi import APIRouter
from sqlalchemy import text

from app.api.dependencies import get_db
from app.cache.redis import redis
from app.config.settings import settings

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    summary="Application Health Check",
)
async def health():
    """
    Basic health endpoint.
    """

    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "timestamp": datetime.utcnow().isoformat(),
        "environment": "development" if settings.DEBUG else "production",
    }


@router.get(
    "/ping",
    summary="Ping",
)
async def ping():
    """
    Simple ping endpoint.
    """

    return {
        "message": "pong"
    }


@router.get(
    "/database",
    summary="Database Health",
)
async def database_health():
    """
    PostgreSQL health check.
    """

    db = next(get_db())

    try:

        db.execute(text("SELECT 1"))

        return {
            "database": "connected",
            "status": "healthy",
        }

    except Exception as e:

        return {
            "database": "disconnected",
            "status": "unhealthy",
            "error": str(e),
        }

    finally:
        db.close()


@router.get(
    "/redis",
    summary="Redis Health",
)
async def redis_health():
    """
    Upstash Redis health check.
    """

    try:

        redis.set("health_check", "ok", ex=10)

        value = redis.get("health_check")

        return {
            "redis": "connected",
            "status": "healthy",
            "response": value,
        }

    except Exception as e:

        return {
            "redis": "disconnected",
            "status": "unhealthy",
            "error": str(e),
        }


@router.get(
    "/system",
    summary="System Information",
)
async def system_info():
    """
    Returns server information.
    """

    return {
        "application": settings.APP_NAME,
        "python_version": platform.python_version(),
        "platform": platform.system(),
        "platform_release": platform.release(),
        "machine": platform.machine(),
    }


@router.get(
    "/ready",
    summary="Readiness Probe",
)
async def readiness():
    """
    Kubernetes / Docker readiness probe.
    """

    try:

        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()

        redis.ping()

        return {
            "ready": True,
            "status": "ready",
        }

    except Exception as e:

        return {
            "ready": False,
            "status": "not_ready",
            "error": str(e),
        }


@router.get(
    "/live",
    summary="Liveness Probe",
)
async def liveness():
    """
    Kubernetes liveness probe.
    """

    return {
        "alive": True
    }