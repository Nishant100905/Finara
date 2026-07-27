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

    Responsibilities
    ----------------
    - Analyze portfolio
    - Evaluate diversification
    - Detect concentration risk
    - Generate rebalancing suggestions
    """

    def run(
        self,
        state: FinancialState,
    ) -> FinancialState:

        logger.info("Portfolio Agent started.")

        portfolio = state.get("portfolio", {})
        profile = state.get("profile", {})

        metadata = state.setdefault("metadata", {})

        try:

            result = portfolio_analyzer.analyze(
                portfolio=portfolio,
                profile=profile,
            )

            if hasattr(result, "model_dump"):
                result = result.model_dump()

            state["portfolio"] = result

            metadata["portfolio_status"] = "completed"

            logger.info("Portfolio Agent completed.")

        except Exception as exc:

            logger.exception("Portfolio Agent failed.")

            metadata["portfolio_status"] = "failed"
            metadata["error"] = str(exc)

            state["portfolio"] = {
                "error": str(exc)
            }

        return state


portfolio_agent = PortfolioAgent()


def portfolio_node(
    state: FinancialState,
) -> FinancialState:
    """
    LangGraph node.
    """
    return portfolio_agent.run(state)