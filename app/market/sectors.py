"""
Sector performance data built on top of real Yahoo Finance quotes.

We sample a representative ticker per sector and aggregate the day's
percentage change into the canonical NSE/BSE sector buckets the UI expects.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Optional

import yfinance as yf

from app.market.yahoo import _safe_fast_info

logger = logging.getLogger(__name__)


# (Display name, representative ticker). Representative tickers are
# chosen so each bucket reflects the day move of that segment. ETFs are
# preferred where possible because they aggregate many constituents and
# are liquid enough to fetch a clean last-price.
SECTOR_PROXIES: list[tuple[str, str]] = [
    ("Technology", "TCS.NS"),
    ("Financials", "HDFCBANK.NS"),
    ("Energy", "RELIANCE.NS"),
    ("Healthcare", "SUNPHARMA.NS"),
    ("Consumer", "ITC.NS"),
    ("Metals", "TATASTEEL.NS"),
    ("Auto", "MARUTI.NS"),
    ("Realty", "DLF.NS"),
]


def _quote_pct(ticker: yf.Ticker) -> Optional[float]:
    """Return today's percent change for a ticker, or None on failure."""

    # `_safe_fast_info` swallows `KeyError: 'exchangeTimezoneName'`
    # which Yahoo returns for some tickers when the 1y history
    # metadata is incomplete.
    try:
        fast = _safe_fast_info(ticker) or {}
    except Exception:
        logger.exception("Sector proxy: fast_info hard failure")
        return None

    last = fast.get("lastPrice")
    prev = fast.get("previousClose")

    if last is None or prev is None or prev == 0:
        return None

    return round(((last - prev) / prev) * 100, 2)


async def get_sector_performance() -> list[dict[str, float | str]]:
    """
    Return today's percent change per sector.

    Each call queries Yahoo Finance in parallel. Failures on any single
    ticker degrade gracefully — that sector is omitted from the result
    rather than returning zeroed-out fake data.
    """

    def _fetch_all() -> list[Optional[float]]:
        results: list[Optional[float]] = []
        for _, symbol in SECTOR_PROXIES:
            try:
                results.append(_quote_pct(yf.Ticker(symbol)))
            except Exception:
                logger.exception("Sector proxy failed: %s", symbol)
                results.append(None)
        return results

    pct_values = await asyncio.to_thread(_fetch_all)

    sectors: list[dict[str, float | str]] = []
    for (name, _symbol), pct in zip(SECTOR_PROXIES, pct_values):
        if pct is None:
            continue
        sectors.append({"name": name, "changePct": pct})

    return sectors


def compute_sentiment(sectors: list[dict[str, float | str]]) -> dict[str, float | str]:
    """
    Derive a fear/greed-style sentiment score from real sector moves.

    Score is mapped onto a 0–100 scale:
      * 50 = neutral
      * +1% average change moves score by ~20 points
      * result clamped to [0, 100]

    The label uses standard buckets:
      * 0–24   Extreme Fear
      * 25–44  Fear
      * 45–55  Neutral
      * 56–74  Greed
      * 75–100 Extreme Greed
    """

    if not sectors:
        return {"score": 50, "label": "Neutral"}

    avg = sum(float(s["changePct"]) for s in sectors) / len(sectors)
    score = int(round(50 + avg * 20))
    score = max(0, min(100, score))

    if score < 25:
        label = "Extreme Fear"
    elif score < 45:
        label = "Fear"
    elif score <= 55:
        label = "Neutral"
    elif score < 75:
        label = "Greed"
    else:
        label = "Extreme Greed"

    return {"score": score, "label": label}