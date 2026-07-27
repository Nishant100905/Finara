"""
Memory Service.

Responsible for managing user conversation memory,
summaries, and AI context construction.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models import (
    ConversationMemory,
    MemorySummary,
)
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.summary_repository import SummaryRepository


class MemoryService:

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.conversations = ConversationRepository(db)
        self.summaries = SummaryRepository(db)

    # ---------------------------------------------------
    # Conversation
    # ---------------------------------------------------

    def save_message(
        self,
        message: ConversationMemory,
    ) -> ConversationMemory:

        return self.conversations.save_message(message)

    def get_thread(
        self,
        user_id: str,
        thread_id: str,
    ):

        return self.conversations.get_conversation(
            user_id,
            thread_id,
        )

    def get_recent_messages(
        self,
        user_id: str,
        limit: int = 20,
    ):

        return self.conversations.get_recent_context(
            user_id=user_id,
            limit=limit,
        )

    def clear_thread(
        self,
        user_id: str,
        thread_id: str,
    ):

        return self.conversations.delete_conversation(
            user_id,
            thread_id,
        )

    # ---------------------------------------------------
    # Summary
    # ---------------------------------------------------

    def get_summary(
        self,
        user_id: str,
    ):

        return self.summaries.get(user_id)

    def save_summary(
        self,
        summary: MemorySummary,
    ):

        return self.summaries.save(summary)

    # ---------------------------------------------------
    # AI Context
    # ---------------------------------------------------

    def build_context(
        self,
        user_id: str,
        limit: int = 15,
    ) -> dict:

        summary = self.get_summary(user_id)

        history = self.get_recent_messages(
            user_id=user_id,
            limit=limit,
        )

        return {

            "summary": (
                summary.summary
                if summary
                else ""
            ),

            "history": [

                {
                    "role": item.role,
                    "message": item.message,
                    "metadata": item.metadata_json,
                }

                for item in history

            ],

        }