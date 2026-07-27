"""
LangChain portfolio tools.
"""

import json

from langchain_core.tools import tool

from app.tools.portfolio_tools import PortfolioAnalyzer

portfolio = PortfolioAnalyzer()


@tool
def analyze_portfolio(holdings: dict) -> str:
    """
    Analyze a portfolio.
    """
    return json.dumps(
        portfolio.analyze(holdings),
        indent=2,
        default=str,
    )


@tool
def rebalance_portfolio(
    holdings: dict,
    max_allocation: float = 30,
) -> str:
    """
    Suggest portfolio rebalancing.
    """
    return json.dumps(
        portfolio.rebalance(
            holdings,
            max_allocation,
        ),
        indent=2,
    )


@tool
def portfolio_summary(
    holdings: dict,
) -> str:
    """
    Portfolio summary.
    """
    return portfolio.summary(
        holdings,
    )