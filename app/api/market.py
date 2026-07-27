import asyncio
from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from app.market.models import SearchResponse
from app.market.news import MarketNewsService
from app.market.sectors import (
    compute_sentiment,
    get_sector_performance,
)
from app.market.yahoo import YahooFinanceService
from app.market.exceptions import SymbolNotFoundError

router = APIRouter()
yahoo = YahooFinanceService()
news_service = MarketNewsService()


def calculate_change_pct(current: float, previous: float) -> float:
    if not current or not previous:
        return 0.0
    return round(((current - previous) / previous) * 100, 2)


async def fetch_quote(symbol_id: str, name: str) -> dict[str, Any]:
    try:
        # Run in thread since YahooFinanceService methods are sync
        stock = await asyncio.to_thread(yahoo.get_stock_info, symbol_id)
        history = await yahoo.get_history(symbol_id, period="1mo")

        current_price = stock.current_price or 0.0
        previous_close = stock.previous_close or current_price

        spark = [h.close for h in history] if history else []

        return {
            "symbol": symbol_id if not symbol_id.startswith("^") else name.upper(),
            "name": name,
            "price": current_price,
            "changePct": calculate_change_pct(current_price, previous_close),
            "spark": spark,
        }
    except Exception:
        # Fallback if fetching fails
        return {
            "symbol": symbol_id if not symbol_id.startswith("^") else name.upper(),
            "name": name,
            "price": 0.0,
            "changePct": 0.0,
            "spark": [],
        }


@router.get("/")
async def get_market_data():
    # Define targets
    indices_targets = [
        ("^NSEI", "NIFTY 50"),
        ("^BSESN", "BSE Sensex"),
        ("^NSEBANK", "Bank Nifty"),
        ("^IXIC", "NASDAQ"),
    ]

    trending_targets = [
        ("RELIANCE.NS", "Reliance Ind."),
        ("TCS.NS", "TCS"),
        ("INFY.NS", "Infosys"),
        ("HDFCBANK.NS", "HDFC Bank"),
        ("TATAMOTORS.NS", "Tata Motors"),
        ("ITC.NS", "ITC Ltd"),
    ]

    crypto_targets = [
        ("BTC-USD", "Bitcoin"),
        ("ETH-USD", "Ethereum"),
        ("SOL-USD", "Solana"),
        ("ADA-USD", "Cardano"),
    ]

    # Fetch all concurrently. Quote panels still come from Yahoo Finance;
    # sectors and headlines now do too — no more hardcoded mocks.
    indices, trending, crypto, sectors, news = await asyncio.gather(
        asyncio.gather(*[fetch_quote(sym, name) for sym, name in indices_targets]),
        asyncio.gather(*[fetch_quote(sym, name) for sym, name in trending_targets]),
        asyncio.gather(*[fetch_quote(sym, name) for sym, name in crypto_targets]),
        get_sector_performance(),
        news_service.market_headlines(limit=8),
    )

    sentiment = compute_sentiment(sectors)

    return {
        "indices": indices,
        "trending": trending,
        "crypto": crypto,
        "sectors": sectors,
        "news": news,
        "sentiment": sentiment,
        "generated_at": datetime.utcnow().isoformat(),
    }


@router.get("/search", response_model=SearchResponse)
async def search_symbols(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=25),
):
    """
    Search for stocks, indices, ETFs, or cryptocurrencies by name or ticker.

    Backed by Yahoo Finance autocomplete (`yfinance.Search`). Returns up
    to `limit` normalized results with symbol, name, exchange, and type.
    """

    query = q.strip()
    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query parameter 'q' must not be empty.",
        )

    results = await yahoo.search(query, limit=limit)

    return SearchResponse(query=query, results=results)


@router.get("/quote")
async def get_quote(
    symbol: str = Query(..., min_length=1),
):
    """
    Return a single stock quote (price + sparkline + change %) by symbol.
    """

    return await fetch_quote(symbol.strip().upper(), symbol.strip().upper())