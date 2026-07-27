"""
Conversation history service.
"""

from __future__ import annotations

from app.memory.manager import memory


class HistoryService:

    def add_user_message(
        self,
        message: str,
    ):

        memory.remember_message(
            "user",
            message,
        )

    def add_ai_message(
        self,
        message: str,
    ):

        memory.remember_message(
            "assistant",
            message,
        )

    def get_history(self):

        return memory.conversation.messages

    def clear(self):

        memory.conversation.messages.clear()


history_service = HistoryService()