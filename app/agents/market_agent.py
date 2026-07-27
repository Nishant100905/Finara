"""
Portfolio Analysis Agent.
"""

from __future__ import annotations

import logging

from app.market.portfolio import portfolio_analyzer
from .state import FinancialState

logger = logging.getLogger(__name__)


class PortfolioAgent:
    """
    Portfolio Analysis Agent.
    """

    def run(
        self,
        state: FinancialState,
    ) -> FinancialState:

        logger.info("Portfolio Agent started.")

        holdings = state.get("portfolio", [])

        try:
            analysis = portfolio_analyzer.analyze(
                holdings=holdings
            )

            state["portfolio"] = analysis.model_dump()

            metadata = state.setdefault("metadata", {})
            metadata["portfolio_status"] = "completed"

            logger.info("Portfolio Agent completed.")

        except Exception as exc:

            logger.exception("Portfolio Agent failed.")

            metadata = state.setdefault("metadata", {})
            metadata["portfolio_status"] = "failed"

            state["portfolio"] = {
                "error": str(exc)
            }

        return state


portfolio_agent = PortfolioAgent()


def market_node(
    state: FinancialState,
) -> FinancialState:
    """
    LangGraph node.
    """
    return portfolio_agent.run(state)