"""
Financial Coach Agent.
"""

from __future__ import annotations

import logging

from app.coach.service import financial_coach_service
from .state import FinancialState

logger = logging.getLogger(__name__)


class CoachAgent:
    """
    Financial Coach Agent.

    Responsibilities
    ----------------
    - Generate personalized financial advice
    - Create nudges
    - Generate financial insights
    - Produce alerts
    """

    def run(
        self,
        state: FinancialState,
    ) -> FinancialState:

        logger.info("Coach Agent started.")

        profile = state.get("profile", {})
        portfolio = state.get("portfolio", {})
        goals = state.get("goals", [])
        health = state.get("financial_health", {})

        try:
            response = financial_coach_service.coach(
                profile=profile,
                goals=goals,
                portfolio=portfolio,
                health=health,
            )

            state["coach"] = response.model_dump()

            metadata = state.setdefault("metadata", {})
            metadata["coach_status"] = "completed"

            logger.info("Coach Agent completed successfully.")

        except Exception as exc:
            logger.exception("Coach Agent failed.")

            metadata = state.setdefault("metadata", {})
            metadata["coach_status"] = "failed"

            state["coach"] = {
                "error": str(exc),
            }

        return state


coach_agent = CoachAgent()


def coach_node(
    state: FinancialState,
) -> FinancialState:
    """
    LangGraph node.
    """

    return coach_agent.run(state)