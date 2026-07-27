"""
Shared state for the Financial AI Multi-Agent System.
"""

from __future__ import annotations

from typing import Any, TypedDict

from langchain_core.messages import BaseMessage


class FinancialState(TypedDict, total=False):
    """
    Shared state passed between all agents.
    """

    messages: list[BaseMessage]

    user_id: str

    query: str

    profile: dict[str, Any]

    goals: list[dict[str, Any]]

    portfolio: dict[str, Any]

    financial_health: dict[str, Any]

    recommendations: list[Any]

    planner: dict[str, Any]

    forecast: dict[str, Any]

    coach: dict[str, Any]

    market: dict[str, Any]

    report: dict[str, Any]

    rag_context: str

    response: str

    next_agent: str

    execution_history: list[str]

    confidence: float

    metadata: dict[str, Any]