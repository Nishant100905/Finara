"""
Execution Planner

Creates an execution plan for the Supervisor.
"""

from __future__ import annotations

import logging

from app.graph.models import (
    AgentType,
    ExecutionPlan,
    ExecutionStrategy,
)

logger = logging.getLogger(__name__)


class ExecutionPlanner:
    """
    Converts intent into an execution plan.
    """

    def create_plan(
        self,
        *,
        intent: str,
        query: str,
    ) -> ExecutionPlan:
        """
        Build an execution plan.

        Future versions can also use:
        - User profile
        - Conversation memory
        - Market state
        """

        intent = intent.lower().strip()
        query = query.lower()

        plan = ExecutionPlan(
            strategy=ExecutionStrategy.SEQUENTIAL,
        )

        # =====================================================
        # Enterprise RAG
        # =====================================================

        if intent == "rag":

            plan.add(
                AgentType.RAG,
                "Answer using enterprise knowledge base.",
            )

            return plan

        # =====================================================
        # Financial
        # =====================================================

        if intent == "financial":

            plan.add(
                AgentType.FINANCIAL,
                "Financial reasoning and tools.",
            )

            return plan

        # =====================================================
        # Hybrid
        # =====================================================

        if intent == "hybrid":

            plan.add(
                AgentType.HYBRID,
                "Combine enterprise RAG with financial tools.",
            )

            return plan

        # =====================================================
        # Future: Portfolio
        # =====================================================

        if any(
            word in query
            for word in (
                "portfolio",
                "allocation",
                "rebalance",
            )
        ):

            plan.add(
                AgentType.FINANCIAL,
                "Portfolio analysis",
            )

            return plan

        # =====================================================
        # Future: Market
        # =====================================================

        if any(
            word in query
            for word in (
                "stock",
                "market",
                "share",
                "price",
            )
        ):

            plan.add(
                AgentType.MARKET,
                "Market analysis",
            )

            plan.add(
                AgentType.FINANCIAL,
                "Investment reasoning",
            )

            return plan

        # =====================================================
        # Default
        # =====================================================

        logger.warning(
            "Unknown intent '%s'. Falling back to RAG.",
            intent,
        )

        plan.add(
            AgentType.RAG,
            "Fallback",
        )

        return plan


planner = ExecutionPlanner()