"""
SQLAlchemy models for AI Financial Memory.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    DateTime,
    Float,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.postgres import Base


# ==========================================================
# Timestamp Mixin
# ==========================================================

class TimestampMixin:

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


# ==========================================================
# User Financial Profile
# ==========================================================

class UserProfile(
    Base,
    TimestampMixin,
):
    __tablename__ = "user_profiles"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        index=True,
        nullable=False,
    )

    income: Mapped[float | None] = mapped_column(Float, nullable=True)
    expenses: Mapped[float | None] = mapped_column(Float, nullable=True)
    savings: Mapped[float | None] = mapped_column(Float, nullable=True)
    monthly_investment: Mapped[float | None] = mapped_column(Float, nullable=True)

    investment_goal: Mapped[str | None] = mapped_column(String(200))
    risk_tolerance: Mapped[str | None] = mapped_column(String(50))
    time_horizon: Mapped[str | None] = mapped_column(String(100))

    preferred_assets: Mapped[list] = mapped_column(
        JSON,
        default=list,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="INR",
    )


# ==========================================================
# Conversation Memory
# ==========================================================

class ConversationMemory(
    Base,
    TimestampMixin,
):
    __tablename__ = "conversation_memory"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(128),
        index=True,
        nullable=False,
    )

    thread_id: Mapped[str] = mapped_column(
        String(128),
        index=True,
    )

    role: Mapped[str] = mapped_column(String(20))

    message: Mapped[str] = mapped_column(Text)

    metadata_json: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
    )


# ==========================================================
# Tool History
# ==========================================================

class ToolHistory(
    Base,
    TimestampMixin,
):
    __tablename__ = "tool_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(128),
        index=True,
    )

    tool_name: Mapped[str] = mapped_column(String(100))

    arguments: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
    )

    result: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
    )


# ==========================================================
# Memory Summary
# ==========================================================

class MemorySummary(
    Base,
    TimestampMixin,
):
    __tablename__ = "memory_summary"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        index=True,
    )

    summary: Mapped[str] = mapped_column(Text)


# ==========================================================
# Uploaded Documents
# ==========================================================

class Document(
    Base,
    TimestampMixin,
):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        String(128),
        index=True,
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    stored_filename: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False,
    )

    file_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    chunk_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    page_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    embedding_model: Mapped[str] = mapped_column(
        String(100),
        default="BAAI/bge-small-en-v1.5",
        nullable=False,
    )

    vector_collection: Mapped[str] = mapped_column(
        String(100),
        default="documents",
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="processing",
        nullable=False,
    )

    metadata_json: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )


# ==========================================================
# Indexes
# ==========================================================

Index(
    "idx_conversation_user_thread",
    ConversationMemory.user_id,
    ConversationMemory.thread_id,
)

Index(
    "idx_tool_history_user",
    ToolHistory.user_id,
)

Index(
    "idx_documents_user",
    Document.user_id,
)