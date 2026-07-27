"""
Market news service.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Iterable

import yfinance as yf

from .models import MarketNews

logger = logging.getLogger(__name__)


# Default tickers sampled to build the market-wide news feed.
DEFAULT_NEWS_SYMBOLS: list[str] = [
    "^NSEI",
    "^BSESN",
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "BTC-USD",
]


def _relative_time(published_at: datetime | None) -> str:
    """Format a datetime as a short, human-readable 'time ago' label."""

    if published_at is None:
        return ""

    # Normalize tz-aware datetimes to UTC-naive so we can subtract
    # from datetime.utcnow(). Yahoo's `pubDate` comes back as
    # tz-aware ISO (with `Z`); our own datetimes elsewhere are naive.
    if published_at.tzinfo is not None:
        published_at = published_at.astimezone(tz=None).replace(tzinfo=None)

    delta = datetime.utcnow() - published_at
    seconds = int(delta.total_seconds())
    if seconds < 60:
        return "Just now"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours}h ago"
    days = hours // 24
    return f"{days}d ago"


class MarketNewsService:
    """
    Yahoo Finance news provider.
    """

    async def get_company_news(
        self,
        symbol: str,
        limit: int = 5,
    ) -> list[MarketNews]:

        return await asyncio.to_thread(
            self._get_company_news,
            symbol,
            limit,
        )

    def _get_company_news(
        self,
        symbol: str,
        limit: int,
    ) -> list[MarketNews]:

        ticker = yf.Ticker(symbol)

        articles = ticker.news or []

        news: list[MarketNews] = []

        for article in articles[:limit]:

            try:

                content = article.get(
                    "content",
                    {},
                )

                provider = content.get(
                    "provider",
                    {},
                )

                published = content.get(
                    "pubDate",
                )

                published_at = None

                if published:

                    try:

                        published_at = (
                            datetime.fromisoformat(
                                published.replace(
                                    "Z",
                                    "+00:00",
                                )
                            )
                        )

                    except Exception:

                        published_at = None

                news.append(
                    MarketNews(
                        title=content.get(
                            "title",
                            "",
                        ),
                        publisher=provider.get(
                            "displayName",
                        ),
                        url=content.get(
                            "canonicalUrl",
                            {},
                        ).get("url"),
                        summary=content.get(
                            "summary",
                        ),
                        published_at=published_at,
                    )
                )

            except Exception:

                logger.exception(
                    "Failed to parse news article."
                )

        return news

    async def market_headlines(
        self,
        symbols: Iterable[str] | None = None,
        *,
        limit: int = 8,
    ) -> list[dict]:
        """
        Aggregate the most recent news across the supplied symbols.

        Returns deduped, chronologically-ordered, UI-ready news items
        rather than `MarketNews` model objects (so we can attach the
        'time ago' label the frontend expects).
        """

        symbols = list(symbols or DEFAULT_NEWS_SYMBOLS)

        per_symbol = await asyncio.gather(
            *[self.get_company_news(s) for s in symbols],
            return_exceptions=True,
        )

        merged: dict[str, dict] = {}
        order: list[str] = []
        for result in per_symbol:
            if isinstance(result, Exception):
                logger.exception("News fetch failed.")
                continue
            for article in result:
                key = (article.title or "").strip()
                if not key or key in merged:
                    continue
                published = article.published_at
                merged[key] = {
                    "id": key,
                    "title": article.title,
                    "source": article.publisher or "Yahoo Finance",
                    "time": _relative_time(published),
                    "tag": "Market",
                    "published_at": (
                        published.isoformat() if published else None
                    ),
                    "url": article.url,
                }
                order.append(key)

        items = [merged[k] for k in order]
        items.sort(
            key=lambda n: n.get("published_at") or "",
            reverse=True,
        )
        return items[:limit]

    async def headlines(
        self,
        symbols: list[str],
    ) -> dict[str, list[MarketNews]]:

        result: dict[
            str,
            list[MarketNews],
        ] = {}

        for symbol in symbols:

            try:

                result[symbol] = (
                    await self.get_company_news(
                        symbol
                    )
                )

            except Exception:

                logger.exception(
                    "Failed to fetch news for %s",
                    symbol,
                )

                result[symbol] = []

        return result