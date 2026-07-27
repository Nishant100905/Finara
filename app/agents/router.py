"""
Intent router for Financial AI agents.
"""

from __future__ import annotations

from enum import Enum


class AgentType(str, Enum):
    """
    Supported agents.
    """

    SUPERVISOR = "supervisor"

    PLANNER = "planner"

    COACH = "coach"

    PORTFOLIO = "portfolio"

    MARKET = "market"

    RESEARCH = "research"

    REPORT = "report"


class AgentRouter:
    """
    Routes a query to the most appropriate agent.
    """

    def route(
        self,
        query: str,
    ) -> AgentType:

        query = query.lower()

        planner_keywords = [
            "budget",
            "save",
            "saving",
            "goal",
            "plan",
            "planning",
            "retirement",
            "sip",
            "investment plan",
        ]

        coach_keywords = [
            "improve",
            "advice",
            "coach",
            "tips",
            "recommend",
            "recommendation",
            "habit",
            "expense",
        ]

        portfolio_keywords = [
            "portfolio",
            "allocation",
            "holdings",
            "rebalance",
            "asset",
            "mutual fund",
            "stock allocation",
        ]

        market_keywords = [
            "market",
            "news",
            "share",
            "stock",
            "nifty",
            "sensex",
            "gold",
            "bitcoin",
            "crypto",
            "price",
        ]

        report_keywords = [
            "report",
            "summary",
            "pdf",
            "excel",
            "statement",
            "financial report",
        ]

        research_keywords = [
            "policy",
            "document",
            "explain",
            "research",
            "what is",
            "why",
            "how",
        ]

        if self._contains(
            query,
            planner_keywords,
        ):
            return AgentType.PLANNER

        if self._contains(
            query,
            coach_keywords,
        ):
            return AgentType.COACH

        if self._contains(
            query,
            portfolio_keywords,
        ):
            return AgentType.PORTFOLIO

        if self._contains(
            query,
            market_keywords,
        ):
            return AgentType.MARKET

        if self._contains(
            query,
            report_keywords,
        ):
            return AgentType.REPORT

        if self._contains(
            query,
            research_keywords,
        ):
            return AgentType.RESEARCH

        return AgentType.SUPERVISOR

    @staticmethod
    def _contains(
        query: str,
        keywords: list[str],
    ) -> bool:

        return any(
            keyword in query
            for keyword in keywords
        )


agent_router = AgentRouter()