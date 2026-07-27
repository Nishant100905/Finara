"""
LangChain tools for portfolio analysis.
"""

from __future__ import annotations

import json
from typing import Dict

from langchain_core.tools import tool

from app.market.analyzer import MarketAnalyzer
from app.market.yahoo import YahooFinanceService


yahoo = YahooFinanceService()
analyzer = MarketAnalyzer()


@tool
def analyze_portfolio(holdings: Dict[str, float]) -> str:
    """
    Analyze a stock portfolio.

    Args:
        holdings:
            Dictionary of ticker -> quantity.

    Example:
        {
            "AAPL": 10,
            "MSFT": 5,
            "GOOGL": 4
        }
    """

    portfolio = []

    total_value = 0.0

    for symbol, quantity in holdings.items():

        stock = yahoo.get_stock_info(symbol)

        price = stock.current_price or 0

        value = price * quantity

        total_value += value

        portfolio.append(
            {
                "symbol": symbol,
                "company": stock.company_name,
                "quantity": quantity,
                "price": price,
                "value": value,
                "sector": stock.sector,
                "beta": stock.beta,
                "market_cap": stock.market_cap,
            }
        )

    sector_allocation = {}

    weighted_beta = 0.0

    for item in portfolio:

        allocation = (
            item["value"] / total_value
            if total_value
            else 0
        )

        item["allocation"] = round(
            allocation * 100,
            2,
        )

        weighted_beta += (
            allocation *
            (item["beta"] or 1)
        )

        sector = item["sector"] or "Unknown"

        sector_allocation.setdefault(
            sector,
            0,
        )

        sector_allocation[sector] += item["allocation"]

    largest_position = max(
        portfolio,
        key=lambda x: x["allocation"],
    )

    report = {
        "portfolio_value": round(
            total_value,
            2,
        ),
        "weighted_beta": round(
            weighted_beta,
            2,
        ),
        "number_of_holdings": len(
            portfolio,
        ),
        "largest_position": largest_position,
        "sector_allocation": sector_allocation,
        "holdings": portfolio,
    }

    return json.dumps(
        report,
        indent=2,
        default=str,
    )


@tool
def rebalance_portfolio(
    holdings: Dict[str, float],
    max_allocation: float = 30.0,
) -> str:
    """
    Suggest portfolio rebalancing.

    max_allocation is in percent.
    """

    report = json.loads(
        analyze_portfolio.invoke(
            {"holdings": holdings}
        )
    )

    suggestions = []

    for stock in report["holdings"]:

        if stock["allocation"] > max_allocation:

            suggestions.append(
                {
                    "symbol": stock["symbol"],
                    "allocation": stock["allocation"],
                    "recommendation":
                        "Reduce exposure",
                }
            )

    if not suggestions:

        return "Portfolio appears well balanced."

    return json.dumps(
        suggestions,
        indent=2,
    )


@tool
def portfolio_summary(
    holdings: Dict[str, float],
) -> str:
    """
    Short summary for the LLM.
    """

    report = json.loads(
        analyze_portfolio.invoke(
            {"holdings": holdings}
        )
    )

    return (
        f"Portfolio value: {report['portfolio_value']}\n"
        f"Holdings: {report['number_of_holdings']}\n"
        f"Weighted beta: {report['weighted_beta']}\n"
        f"Largest position: "
        f"{report['largest_position']['company']}"
    )