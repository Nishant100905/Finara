"""
AI Daily Summary Generator.
"""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate

from app.llm import llm
from .models import DailySummary


class AISummaryGenerator:

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert financial advisor.

Write a concise daily financial briefing.

Requirements:

- Professional tone
- 150-250 words
- Mention financial health
- Mention goals
- Mention important insights
- Finish with one actionable recommendation
""",
            ),
            (
                "human",
                """
Financial Health:
{health}

Insights:
{insights}

Goals:
{goals}
""",
            ),
        ]
    )

    @classmethod
    def generate(
        cls,
        summary: DailySummary,
    ) -> str:

        chain = cls.prompt | llm

        response = chain.invoke(
            {
                "health": summary.financial_health,
                "insights": "\n".join(
                    section.content for section in summary.sections
                ),
                "goals": "\n".join(summary.recommendations),
            }
        )

        return response.content
