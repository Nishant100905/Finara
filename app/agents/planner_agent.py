"""
Financial Planner Agent.
"""

from __future__ import annotations

import logging
from typing import Any

from .state import FinancialState
from app.planner.service import financial_planner_service

logger = logging.getLogger(__name__)


class PlannerAgent:
    """
    Planner Agent responsible for creating
    financial plans and roadmaps.
    """

    def run(
        self,
        state: FinancialState,
    ) -> FinancialState:

        logger.info(
            "Planner Agent started."
        )

        profile = state.get(
            "profile",
            {},
        )

        portfolio = state.get(
            "portfolio",
            {},
        )

        goals = state.get(
            "goals",
            [],
        )

        try:

            planner_response = (
                financial_planner_service.forecast(
                    profile=profile,
                    portfolio=portfolio,
                    goals=goals,
                )
            )

            state["planner"] = planner_response.model_dump()

            state.setdefault(
                "metadata",
                {},
            )["planner_status"] = "completed"

            logger.info(
                "Planner Agent completed successfully."
            )

        except Exception as exc:

            logger.exception(
                "Planner Agent failed."
            )

            state.setdefault(
                "metadata",
                {},
            )["planner_status"] = "failed"

            state["planner"] = {
                "error": str(exc),
            }

        return state


planner_agent = PlannerAgent()


def planner_node(
    state: FinancialState,
) -> FinancialState:
    """
    LangGraph node.
    """

    return planner_agent.run(
        state,
    )