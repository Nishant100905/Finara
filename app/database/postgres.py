"""
PostgreSQL Database Configuration
Production Ready
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config.settings import settings

# ==========================================================
# SQLAlchemy Base
# ==========================================================

Base = declarative_base()

# Import models AFTER Base is created
from app.database import models  # noqa: E402,F401

# ==========================================================
# Engine
# ==========================================================

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    future=True,
    connect_args={
        "sslmode": settings.DATABASE_SSLMODE,
    },
)

# ==========================================================
# Session
# ==========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# ==========================================================
# Dependency
# ==========================================================

def get_db():
    """
    Database dependency
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================================================
# Database Initialization
# ==========================================================

def create_tables():
    """
    Create all database tables.
    NOTE:
    During development this is fine.
    For production, use Alembic migrations.
    """

    Base.metadata.create_all(bind=engine)


# ==========================================================
# Health Check
# ==========================================================

def check_database_connection() -> bool:
    """
    Check if PostgreSQL is reachable.
    Returns True if healthy, otherwise False.
    """

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True

    except Exception:
        return False