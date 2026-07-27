"""
Financial Multi-Agent Service.

Entry point for interacting with the LangGraph
Financial Multi-Agent System.
"""

from __future__ import annotations

import logging
from typing import Any

from .graph import financial_agent_graph
from .state import FinancialState

logger = logging.getLogger(__name__)


class MultiAgentService:
    """
    Executes the Financial Multi-Agent LangGraph workflow.
    """

    def __init__(self) -> None:
        self.graph = financial_agent_graph

    def _build_state(
        self,
        *,
        user_id: str,
        query: str,
        **kwargs: Any,
    ) -> FinancialState:

        return FinancialState(

            messages=[],

            user_id=user_id,

            query=query,

            profile=kwargs.get(
                "profile",
                {},
            ),

            goals=kwargs.get(
                "goals",
                [],
            ),

            portfolio=kwargs.get(
                "portfolio",
                {},
            ),

            financial_health=kwargs.get(
                "financial_health",
                {},
            ),

            recommendations=kwargs.get(
                "recommendations",
                [],
            ),

            planner={},

            forecast={},

            coach={},

            market={},

            report={},

            rag_context=kwargs.get(
                "rag_context",
                "",
            ),

            response="",

            next_agent="supervisor",

            execution_history=[],

            confidence=0.0,

            metadata={},
        )

    def invoke(
        self,
        *,
        user_id: str,
        query: str,
        **kwargs: Any,
    ) -> FinancialState:

        logger.info(
            "Executing Financial Multi-Agent workflow."
        )

        state = self._build_state(
            user_id=user_id,
            query=query,
            **kwargs,
        )

        result = self.graph.invoke(
            state,
        )

        logger.info(
            "Workflow execution completed."
        )

        return result

    async def ainvoke(
        self,
        *,
        user_id: str,
        query: str,
        **kwargs: Any,
    ) -> FinancialState:

        logger.info(
            "Executing async Financial Multi-Agent workflow."
        )

        state = self._build_state(
            user_id=user_id,
            query=query,
            **kwargs,
        )

        result = await self.graph.ainvoke(
            state,
        )

        logger.info(
            "Async workflow execution completed."
        )

        return result

    def chat(
        self,
        *,
        user_id: str,
        message: str,
        **kwargs: Any,
    ) -> str:

        result = self.invoke(
            user_id=user_id,
            query=message,
            **kwargs,
        )

        return result.get(
            "response",
            "",
        )

    async def achat(
        self,
        *,
        user_id: str,
        message: str,
        **kwargs: Any,
    ) -> str:

        result = await self.ainvoke(
            user_id=user_id,
            query=message,
            **kwargs,
        )

        return result.get(
            "response",
            "",
        )


multi_agent_service = MultiAgentService()