"""
Conversation Memory Repository.
"""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database.models import ConversationMemory

from .base import BaseRepository


class MemoryRepository(
    BaseRepository[ConversationMemory],
):

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

    def save(
        self,
        memory: ConversationMemory,
    ) -> ConversationMemory:

        return self.add(memory)

    def get_history(
        self,
        user_id: str,
        limit: int = 20,
    ) -> Sequence[ConversationMemory]:

        return (
            self.db.query(ConversationMemory)
            .filter(
                ConversationMemory.user_id == user_id
            )
            .order_by(
                desc(ConversationMemory.created_at)
            )
            .limit(limit)
            .all()
        )

    def get_thread(
        self,
        user_id: str,
        thread_id: str,
    ) -> Sequence[ConversationMemory]:

        return (
            self.db.query(ConversationMemory)
            .filter(
                ConversationMemory.user_id == user_id,
                ConversationMemory.thread_id == thread_id,
            )
            .order_by(
                ConversationMemory.created_at.asc()
            )
            .all()
        )

    def delete_thread(
        self,
        user_id: str,
        thread_id: str,
    ) -> int:

        deleted = (
            self.db.query(ConversationMemory)
            .filter(
                ConversationMemory.user_id == user_id,
                ConversationMemory.thread_id == thread_id,
            )
            .delete(
                synchronize_session=False,
            )
        )

        self.commit()

        return deleted

    def clear_user_memory(
        self,
        user_id: str,
    ) -> int:

        deleted = (
            self.db.query(ConversationMemory)
            .filter(
                ConversationMemory.user_id == user_id
            )
            .delete(
                synchronize_session=False,
            )
        )

        self.commit()

        return deleted


memory_repository = MemoryRepository