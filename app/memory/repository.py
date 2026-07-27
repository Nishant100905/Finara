"""
Memory Repository

Persistent memory CRUD operations using SQLAlchemy 2.0.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import (
    ConversationMemory,
    MemorySummary,
    ToolHistory,
    UserProfile,
)


class MemoryRepository:

    def __init__(self, db: Session):
        self.db = db

    # ==========================================================
    # User Profile
    # ==========================================================

    def get_profile(self, user_id: str) -> UserProfile | None:

        stmt = select(UserProfile).where(
            UserProfile.user_id == user_id
        )

        return self.db.execute(stmt).scalar_one_or_none()

    def create_profile(self, profile: UserProfile) -> UserProfile:

        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)

        return profile

    def update_profile(
        self,
        profile: UserProfile,
        **kwargs,
    ) -> UserProfile:

        for key, value in kwargs.items():
            setattr(profile, key, value)

        self.db.commit()
        self.db.refresh(profile)

        return profile

    def delete_profile(self, profile: UserProfile):

        self.db.delete(profile)
        self.db.commit()

    # ==========================================================
    # Conversation History
    # ==========================================================

    def add_message(
        self,
        *,
        user_id: str,
        thread_id: str,
        role: str,
        message: str,
        metadata: dict | None = None,
    ) -> ConversationMemory:

        memory = ConversationMemory(
            user_id=user_id,
            thread_id=thread_id,
            role=role,
            message=message,
            metadata_json=metadata or {},
        )

        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)

        return memory

    def get_history(
        self,
        *,
        user_id: str,
        thread_id: str,
        limit: int = 20,
    ) -> list[ConversationMemory]:

        stmt = (
            select(ConversationMemory)
            .where(
                ConversationMemory.user_id == user_id,
                ConversationMemory.thread_id == thread_id,
            )
            .order_by(
                ConversationMemory.created_at.desc()
            )
            .limit(limit)
        )

        return list(self.db.scalars(stmt).all())

    def clear_history(
        self,
        *,
        user_id: str,
        thread_id: str,
    ):

        messages = self.get_history(
            user_id=user_id,
            thread_id=thread_id,
            limit=100000,
        )

        for message in messages:
            self.db.delete(message)

        self.db.commit()

    # ==========================================================
    # Conversation Summary
    # ==========================================================

    def get_summary(
        self,
        user_id: str,
    ) -> MemorySummary | None:

        stmt = select(MemorySummary).where(
            MemorySummary.user_id == user_id
        )

        return self.db.execute(stmt).scalar_one_or_none()

    def save_summary(
        self,
        *,
        user_id: str,
        summary: str,
    ) -> MemorySummary:

        existing = self.get_summary(user_id)

        if existing:

            existing.summary = summary

            self.db.commit()
            self.db.refresh(existing)

            return existing

        new_summary = MemorySummary(
            user_id=user_id,
            summary=summary,
        )

        self.db.add(new_summary)
        self.db.commit()
        self.db.refresh(new_summary)

        return new_summary

    # ==========================================================
    # Tool History
    # ==========================================================

    def add_tool_history(
        self,
        *,
        user_id: str,
        tool_name: str,
        arguments: dict,
        result: dict,
    ) -> ToolHistory:

        tool = ToolHistory(
            user_id=user_id,
            tool_name=tool_name,
            arguments=arguments,
            result=result,
        )

        self.db.add(tool)
        self.db.commit()
        self.db.refresh(tool)

        return tool

    def get_tool_history(
        self,
        *,
        user_id: str,
        limit: int = 20,
    ) -> list[ToolHistory]:

        stmt = (
            select(ToolHistory)
            .where(
                ToolHistory.user_id == user_id
            )
            .order_by(
                ToolHistory.created_at.desc()
            )
            .limit(limit)
        )

        return list(self.db.scalars(stmt).all())