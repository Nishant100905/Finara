"""
Yahoo Finance provider.
"""

from __future__ import annotations

import asyncio
import logging

import yfinance as yf

from .exceptions import (
    ProviderUnavailableError,
    SymbolNotFoundError,
)
from .models import (
    HistoricalPrice,
    QuoteResponse,
    StockInfo,
)

logger = logging.getLogger(__name__)


def _safe_fast_info(ticker: yf.Ticker) -> dict:
    """
    Return `ticker.fast_info` as a plain dict, never raising.

    Yahoo occasionally serves a ticker whose 1-year history metadata
    is missing keys like `exchangeTimezoneName`. When that happens,
    `Quote.last_price` raises `KeyError: 'exchangeTimezoneName'`
    which would otherwise kill the calling coroutine. Fall back to
    the slower `ticker.info` payload (which still contains last
    price for most tickers) and finally to an empty dict.

    See: yfinance/scrapers/quote.py -> Quote.last_price -> _get_1y_prices.
    """

    # 1. Try the fast path. Catch the specific metadata KeyError plus
    #    any other yfinance quirk (JSON decode, network, etc.) without
    #    letting it propagate.
    try:
        fast = ticker.fast_info
        return dict(fast) if fast else {}
    except KeyError:
        logger.warning(
            "fast_info metadata missing keys for %s; falling back to .info",
            ticker.ticker or "?",
        )
    except Exception:
        logger.exception(
            "fast_info failed for %s; falling back to .info",
            ticker.ticker or "?",
        )

    # 2. Slow fallback. `info` is a large dict from the quoteSummary
    #    endpoint — different code path that doesn't require the
    #    history metadata block.
    try:
        return dict(ticker.info or {})
    except Exception:
        logger.exception(
            "info fallback failed for %s", ticker.ticker or "?"
        )
        return {}


class YahooFinanceService:

    async def get_quote(
        self,
        symbol: str,
    ) -> QuoteResponse:

        stock = await asyncio.to_thread(
            self.get_stock_info,
            symbol,
        )

        return QuoteResponse(
            data=stock,
            source="Yahoo Finance",
            cached=False,
        )

    def get_stock_info(
        self,
        symbol: str,
    ) -> StockInfo:

        try:

            ticker = yf.Ticker(symbol)

            fast = _safe_fast_info(ticker)

            info = ticker.info or {}

            if not fast and not info:
                raise SymbolNotFoundError(symbol)

            return StockInfo(

                symbol=symbol,

                company_name=info.get("longName"),

                exchange=info.get("exchange"),

                sector=info.get("sector"),

                industry=info.get("industry"),

                currency=info.get("currency", "INR"),

                current_price=fast.get(
                    "lastPrice",
                    info.get("currentPrice"),
                ),

                previous_close=fast.get(
                    "previousClose",
                    info.get("previousClose"),
                ),

                open_price=fast.get(
                    "open",
                    info.get("open"),
                ),

                day_high=fast.get(
                    "dayHigh",
                    info.get("dayHigh"),
                ),

                day_low=fast.get(
                    "dayLow",
                    info.get("dayLow"),
                ),

                fifty_two_week_high=fast.get(
                    "yearHigh",
                    info.get("fiftyTwoWeekHigh"),
                ),

                fifty_two_week_low=fast.get(
                    "yearLow",
                    info.get("fiftyTwoWeekLow"),
                ),

                volume=fast.get(
                    "lastVolume",
                    info.get("volume"),
                ),

                average_volume=info.get(
                    "averageVolume"
                ),

                market_cap=fast.get(
                    "marketCap",
                    info.get("marketCap"),
                ),

                enterprise_value=info.get(
                    "enterpriseValue"
                ),

                pe_ratio=info.get(
                    "trailingPE"
                ),

                forward_pe=info.get(
                    "forwardPE"
                ),

                peg_ratio=info.get(
                    "pegRatio"
                ),

                price_to_book=info.get(
                    "priceToBook"
                ),

                eps=info.get(
                    "trailingEps"
                ),

                dividend_yield=info.get(
                    "dividendYield"
                ),

                beta=info.get(
                    "beta"
                ),

                roe=info.get(
                    "returnOnEquity"
                ),

                profit_margin=info.get(
                    "profitMargins"
                ),

                revenue_growth=info.get(
                    "revenueGrowth"
                ),

                debt_to_equity=info.get(
                    "debtToEquity"
                ),

                website=info.get(
                    "website"
                ),

                summary=info.get(
                    "longBusinessSummary"
                ),
            )

        except SymbolNotFoundError:
            raise

        except Exception as exc:

            logger.exception(
                "Yahoo provider failed for %s",
                symbol,
            )

            raise ProviderUnavailableError(
                "Yahoo Finance unavailable."
            ) from exc

    async def get_history(
        self,
        symbol: str,
        period: str = "6mo",
    ) -> list[HistoricalPrice]:

        return await asyncio.to_thread(
            self._history,
            symbol,
            period,
        )

    def _history(
        self,
        symbol: str,
        period: str,
    ) -> list[HistoricalPrice]:

        ticker = yf.Ticker(symbol)

        history = ticker.history(period=period)

        if history.empty:
            raise SymbolNotFoundError(symbol)

        return [
            HistoricalPrice(
                date=index.to_pydatetime(),
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                volume=int(row["Volume"]),
            )
            for index, row in history.iterrows()
        ]

    async def validate_symbol(
        self,
        symbol: str,
    ) -> bool:

        return await asyncio.to_thread(
            self._validate,
            symbol,
        )

    def _validate(
        self,
        symbol: str,
    ) -> bool:

        try:

            ticker = yf.Ticker(symbol)

            return bool(ticker.fast_info)

        except Exception:

            return False

    async def search(
        self,
        query: str,
        *,
        limit: int = 10,
    ) -> list[dict]:
        """
        Resolve a free-text query (company name or ticker) to a list of
        candidate Yahoo Finance quotes.

        Backed by `yfinance.Search`, which proxies Yahoo's autocomplete
        API. Returns a normalized list suitable for `SymbolResolver.search`.
        """

        return await asyncio.to_thread(
            self._search,
            query,
            limit,
        )

    def _search(
        self,
        query: str,
        limit: int,
    ) -> list[dict]:

        try:
            results = yf.Search(query, max_results=max(limit * 2, 20)).quotes or []
        except Exception:
            logger.exception("Yahoo Search failed for %s", query)
            return []

        normalized: list[dict] = []
        for quote in results:

            symbol = quote.get("symbol")
            if not symbol:
                continue

            quote_type = (quote.get("quoteType") or "").upper()
            # Only surface tradeable instruments — skip ETFs-of-ETFs,
            # futures, options chains, currencies, etc. That keeps the
            # autocomplete list focused on actual equities and indices.
            if quote_type not in {"EQUITY", "INDEX", "ETF", "MUTUALFUND", "CRYPTOCURRENCY"}:
                continue

            normalized.append(
                {
                    "symbol": symbol,
                    "name": quote.get("longname") or quote.get("shortname") or symbol,
                    "exchange": quote.get("exchDisp") or quote.get("exchange"),
                    "type": quote.get("quoteType"),
                    "score": quote.get("score"),
                }
            )

            if len(normalized) >= limit:
                break

        return normalized