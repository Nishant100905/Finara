"""
Conversation Repository.

Provides high-level conversation operations
built on top of ConversationMemory.
"""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import desc

from sqlalchemy.orm import Session

from app.database.models import ConversationMemory

from .base import BaseRepository


class ConversationRepository(
    BaseRepository[ConversationMemory],
):

    def __init__(
        self,
        db: Session,
    ):

        super().__init__(db)

    def save_message(
        self,
        message: ConversationMemory,
    ) -> ConversationMemory:

        return self.add(message)

    def get_conversation(
        self,
        user_id: str,
        thread_id: str,
    ) -> Sequence[ConversationMemory]:

        return (
            self.db.query(
                ConversationMemory
            )
            .filter(
                ConversationMemory.user_id == user_id,
                ConversationMemory.thread_id == thread_id,
            )
            .order_by(
                ConversationMemory.created_at.asc()
            )
            .all()
        )

    def list_threads(
        self,
        user_id: str,
        limit: int = 25,
    ) -> list[str]:

        rows = (
            self.db.query(
                ConversationMemory.thread_id
            )
            .filter(
                ConversationMemory.user_id == user_id
            )
            .distinct()
            .order_by(
                desc(
                    ConversationMemory.created_at
                )
            )
            .limit(limit)
            .all()
        )

        return [
            row[0]
            for row in rows
        ]

    def recent_messages(
        self,
        user_id: str,
        limit: int = 50,
    ) -> Sequence[ConversationMemory]:

        return (
            self.db.query(
                ConversationMemory
            )
            .filter(
                ConversationMemory.user_id == user_id
            )
            .order_by(
                desc(
                    ConversationMemory.created_at
                )
            )
            .limit(limit)
            .all()
        )

    def delete_conversation(
        self,
        user_id: str,
        thread_id: str,
    ) -> int:

        deleted = (
            self.db.query(
                ConversationMemory
            )
            .filter(
                ConversationMemory.user_id == user_id,
                ConversationMemory.thread_id == thread_id,
            )
            .delete(
                synchronize_session=False
            )
        )

        self.commit()

        return deleted

    def conversation_count(
        self,
        user_id: str,
    ) -> int:

        return (
            self.db.query(
                ConversationMemory
            )
            .filter(
                ConversationMemory.user_id == user_id
            )
            .count()
        )


conversation_repository = ConversationRepository
def get_last_message(
    self,
    user_id: str,
) -> ConversationMemory | None:
    return (
        self.db.query(ConversationMemory)
        .filter(
            ConversationMemory.user_id == user_id
        )
        .order_by(
            ConversationMemory.created_at.desc()
        )
        .first()
    )
def get_recent_context(
    self,
    user_id: str,
    limit: int = 15,
):
    messages = (
        self.db.query(ConversationMemory)
        .filter(
            ConversationMemory.user_id == user_id
        )
        .order_by(
            ConversationMemory.created_at.desc()
        )
        .limit(limit)
        .all()
    )

    return list(reversed(messages))
def search_messages(
    self,
    user_id: str,
    keyword: str,
):
    return (
        self.db.query(ConversationMemory)
        .filter(
            ConversationMemory.user_id == user_id,
            ConversationMemory.message.ilike(
                f"%{keyword}%"
            ),
        )
        .all()
    )
def clear_user(
    self,
    user_id: str,
):
    deleted = (
        self.db.query(
            ConversationMemory
        )
        .filter(
            ConversationMemory.user_id == user_id
        )
        .delete(
            synchronize_session=False
        )
    )

    self.commit()

    return deleted