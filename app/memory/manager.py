"""
Memory Manager

High-level interface for persistent memory.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.memory.repository import MemoryRepository
from app.memory.service import MemoryService


class MemoryManager:
    """
    Entry point used by the Financial Agent and LangGraph.
    """

    def __init__(self, db: Session):

        self.repository = MemoryRepository(db)
        self.service = MemoryService(self.repository)

    # ==========================================================
    # Conversation
    # ==========================================================

    def remember(
        self,
        *,
        user_id: str,
        thread_id: str,
        message: str,
    ):

        return self.service.process_message(
            user_id=user_id,
            thread_id=thread_id,
            message=message,
        )

    # ==========================================================
    # Profile
    # ==========================================================

    def get_profile(
        self,
        user_id: str,
    ):

        return self.repository.get_profile(user_id)

    # ==========================================================
    # History
    # ==========================================================

    def get_history(
        self,
        *,
        user_id: str,
        thread_id: str,
        limit: int = 20,
    ):

        return self.repository.get_history(
            user_id=user_id,
            thread_id=thread_id,
            limit=limit,
        )

    # ==========================================================
    # Summary
    # ==========================================================

    def get_summary(
        self,
        user_id: str,
    ):

        return self.repository.get_summary(user_id)

    # ==========================================================
    # Tool History
    # ==========================================================

    def get_tool_history(
        self,
        *,
        user_id: str,
        limit: int = 20,
    ):

        return self.repository.get_tool_history(
            user_id=user_id,
            limit=limit,
        )