"""
Memory models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class FinancialProfile:
    income: float | None = None
    expenses: float | None = None
    savings: float | None = None
    monthly_investment: float | None = None

    risk_tolerance: str | None = None
    investment_goal: str | None = None
    time_horizon: str | None = None

    preferred_assets: list[str] = field(default_factory=list)


@dataclass
class ConversationMemory:
    messages: list[dict[str, str]] = field(default_factory=list)

    def add(
        self,
        role: str,
        content: str,
    ):

        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )


@dataclass
class ToolMemory:
    history: list[dict[str, Any]] = field(default_factory=list)

    def add(
        self,
        tool: str,
        result: Any,
    ):

        self.history.append(
            {
                "tool": tool,
                "result": result,
            }
        )