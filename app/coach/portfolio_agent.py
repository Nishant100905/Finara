"""
Portfolio Analysis Agent.
"""

from __future__ import annotations

import logging

from app.market.portfolio import portfolio_analyzer

from app.agents.state import FinancialState

logger = logging.getLogger(__name__)


class PortfolioAgent:
    """
    Portfolio Analysis Agent.

    Responsibilities

    - Analyze holdings
    - Evaluate diversification
    - Detect concentration risk
    - Recommend rebalancing
    """

    def run(
        self,
        state: FinancialState,
    ) -> FinancialState:

        logger.info(
            "Portfolio Agent started."
        )

        portfolio = state.get(
            "portfolio",
            {},
        )

        profile = state.get(
            "profile",
            {},
        )

        try:

            analysis = portfolio_analyzer.analyze(

                portfolio=portfolio,

                profile=profile,

            )

            state["portfolio"] = analysis.model_dump()

            metadata = state.setdefault(
                "metadata",
                {},
            )

            metadata[
                "portfolio_status"
            ] = "completed"

            logger.info(
                "Portfolio Agent completed."
            )

        except Exception as exc:

            logger.exception(
                "Portfolio Agent failed."
            )

            state.setdefault(
                "metadata",
                {},
            )[
                "portfolio_status"
            ] = "failed"

            state["portfolio"] = {

                "error": str(exc)

            }

        return state


portfolio_agent = PortfolioAgent()


def portfolio_node(
    state: FinancialState,
) -> FinancialState:

    return portfolio_agent.run(
        state,
    )