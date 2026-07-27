"""
Enterprise RAG System

Application Entry Point
"""

from contextlib import asynccontextmanager
from app.api.documents import router as documents_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.upload import router as upload_router
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.market import router as market_router

from app.config.logging import setup_logging
from app.config.settings import settings

from app.database.postgres import create_tables
from app.graph.builder import build_graph
from app.rag.bm25 import bm25

logger = setup_logging()


# ==========================================================
# Startup / Shutdown
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("=" * 60)
    logger.info("Starting Enterprise RAG System")
    logger.info("=" * 60)

    # ------------------------------------------------------
    # Database
    # ------------------------------------------------------

    try:
        create_tables()
        logger.info("Database Initialized")

    except Exception as e:
        logger.exception("Database initialization failed")
        logger.exception(e)

    # ------------------------------------------------------
    # LangGraph
    # ------------------------------------------------------

    try:
        app.state.graph = build_graph()
        logger.info("LangGraph Initialized")

    except Exception as e:
        logger.exception("LangGraph initialization failed")
        logger.exception(e)

    # ------------------------------------------------------
    # BM25
    # ------------------------------------------------------

    try:
        from app.graph.nodes.retrieve import initialize_bm25
        initialize_bm25()
        logger.info("BM25 Initialized")

    except Exception as e:
        logger.exception("BM25 initialization failed")
        logger.exception(e)

    yield

    logger.info("Application Shutdown")


# ==========================================================
# FastAPI
# ==========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# ==========================================================
# CORS
# ==========================================================
# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ==========================================================
# Routers
# ==========================================================
app.include_router(
    upload_router,
    prefix="/api/documents",
    tags=["Documents"],
)

app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Authentication"],
)
app.include_router(
    documents_router,
    prefix="/api",
)
app.include_router(
    chat_router,
    prefix="/api/chat",
    tags=["Chat"],
)

app.include_router(
    health_router,
    prefix="/api/health",
    tags=["Health"],
)

app.include_router(
    market_router,
    prefix="/api/market",
    tags=["Market"],
)

# ==========================================================
# Root Endpoint
# ==========================================================


@app.get("/")
async def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }


# ==========================================================
# Ping Endpoint
# ==========================================================


@app.get("/ping")
async def ping():
    return {
        "message": "pong"
    }


# ==========================================================
# Global Exception Handler
# ==========================================================


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):

    logger.exception(exc)

    return {
        "success": False,
        "message": str(exc),
    }