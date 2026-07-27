"""
LangChain tools for live stock analysis.
"""

from __future__ import annotations

import json

from langchain_core.tools import tool

from app.market.analyzer import MarketAnalyzer
from app.market.cache import MarketCache
from app.market.resolver import SymbolResolver
from app.market.yahoo import YahooFinanceService

yahoo = YahooFinanceService()
cache = MarketCache()
analyzer = MarketAnalyzer()
resolver = SymbolResolver()


@tool
async def analyze_stock(query: str) -> str:
    """
    Analyze a stock using live Yahoo Finance data.

    Examples:
        analyze_stock("Apple")
        analyze_stock("Reliance")
        analyze_stock("AAPL")
        analyze_stock("RELIANCE.NS")
    """

    symbol = await resolver.resolve(query)

    cached = cache.get("stock", symbol)

    if cached:
        if isinstance(cached, str):
            return cached
        return json.dumps(cached, indent=2, default=str)

    stock = yahoo.get_stock_info(symbol)

    history = await yahoo.get_history(symbol)

    report = {
        "symbol": stock.symbol,
        "company": stock.company_name,
        "price": stock.current_price,
        "currency": stock.currency,
        "market_cap": stock.market_cap,
        "pe_ratio": stock.pe_ratio,
        "forward_pe": stock.forward_pe,
        "eps": stock.eps,
        "beta": stock.beta,
        "52_week_high": stock.fifty_two_week_high,
        "52_week_low": stock.fifty_two_week_low,
        "trend": analyzer.trend(history),
        "volatility": analyzer.volatility(history),
        "valuation": analyzer.valuation(stock),
        "risk": analyzer.risk(stock),
        "summary": analyzer.generate_summary(
            stock,
            history,
        ),
    }

    cache.set(
        "stock",
        symbol,
        report,
    )

    result = json.dumps(
        report,
        indent=2,
        default=str,
    )

    return result


@tool
async def compare_stocks(
    stock1: str,
    stock2: str,
) -> str:
    """
    Compare two stocks.

    Examples:
        compare_stocks("Apple", "Microsoft")
        compare_stocks("Reliance", "Infosys")
    """

    symbol1 = await resolver.resolve(stock1)
    symbol2 = await resolver.resolve(stock2)

    first = yahoo.get_stock_info(symbol1)
    second = yahoo.get_stock_info(symbol2)

    comparison = {
        first.company_name: {
            "symbol": first.symbol,
            "price": first.current_price,
            "market_cap": first.market_cap,
            "pe_ratio": first.pe_ratio,
            "beta": first.beta,
            "sector": first.sector,
            "industry": first.industry,
        },
        second.company_name: {
            "symbol": second.symbol,
            "price": second.current_price,
            "market_cap": second.market_cap,
            "pe_ratio": second.pe_ratio,
            "beta": second.beta,
            "sector": second.sector,
            "industry": second.industry,
        },
    }

    return json.dumps(
        comparison,
        indent=2,
        default=str,
    )


@tool
async def stock_price(
    query: str,
) -> str:
    """
    Get the live stock price.

    Examples:
        stock_price("Tesla")
        stock_price("TCS")
    """

    symbol = await resolver.resolve(query)

    stock = yahoo.get_stock_info(symbol)

    return (
        f"{stock.company_name} "
        f"({stock.symbol}) is currently trading at "
        f"{stock.current_price} "
        f"{stock.currency}."
    )


@tool
async def search_stock(
    query: str,
) -> str:
    """
    Search for stocks by company name.

    Example:
        search_stock("Reliance")
        search_stock("Apple")
    """

    results = await resolver.search(query)

    if not results:
        return "No matching stocks found."

    return json.dumps(
        results,
        indent=2,
    )


@tool
async def suggest_stocks(
    query: str,
) -> str:
    """
    Suggest stock names from partial input.

    Example:
        suggest_stocks("Mic")
    """

    suggestions = await resolver.suggest(query)

    if not suggestions:
        return "No suggestions found."

    return json.dumps(
        suggestions,
        indent=2,
    )