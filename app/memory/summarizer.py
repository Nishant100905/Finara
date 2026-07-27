"""
Conversation Summarizer
"""

from __future__ import annotations

from app.llm import llm
from app.memory.repository import MemoryRepository


SUMMARY_PROMPT = """
You are an AI memory summarizer.

Summarize the conversation.

Keep only:

- User profile
- Financial goals
- Income
- Expenses
- Risk tolerance
- Investments
- Important decisions

Ignore greetings and small talk.

Return less than 300 words.
"""


class ConversationSummarizer:

    def __init__(self, repository: MemoryRepository):

        self.repository = repository

    def summarize(
        self,
        user_id: str,
        thread_id: str,
    ):

        history = self.repository.get_history(
            user_id=user_id,
            thread_id=thread_id,
            limit=100,
        )

        if not history:
            return ""

        conversation = "\n".join(
            f"{m.role}: {m.message}"
            for m in history
        )

        response = llm.invoke(
            SUMMARY_PROMPT + "\n\n" + conversation
        )

        summary = response.content

        self.repository.save_summary(
            user_id=user_id,
            summary=summary,
        )

        return summary