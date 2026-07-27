"""
Market repository.

Acts as the single source of truth for market data.
Handles caching before calling external providers.
"""

from __future__ import annotations

import logging

from .cache import MarketCache
from .models import (
    HistoricalPrice,
    QuoteResponse,
)
from .yahoo import YahooFinanceService

logger = logging.getLogger(__name__)


class MarketRepository:

    def __init__(self):

        self.provider = YahooFinanceService()

        self.cache = MarketCache()

    async def get_quote(
        self,
        symbol: str,
        *,
        use_cache: bool = True,
    ) -> QuoteResponse:

        if use_cache:

            cached = self.cache.get(
                "quote",
                symbol,
            )

            if cached:

                logger.debug(
                    "Quote cache hit: %s",
                    symbol,
                )

                response = QuoteResponse.model_validate(
                    cached
                )

                response.cached = True

                return response

        logger.debug(
            "Quote cache miss: %s",
            symbol,
        )

        quote = await self.provider.get_quote(
            symbol
        )

        self.cache.set(
            "quote",
            symbol,
            quote,
        )

        return quote

    async def get_history(
        self,
        symbol: str,
        period: str = "6mo",
    ) -> list[HistoricalPrice]:

        return await self.provider.get_history(
            symbol,
            period,
        )

    async def validate_symbol(
        self,
        symbol: str,
    ) -> bool:

        return await self.provider.validate_symbol(
            symbol,
        )

    def invalidate_quote(
        self,
        symbol: str,
    ) -> None:

        self.cache.delete(
            "quote",
            symbol,
        )

    def clear_cache(self) -> None:

        self.cache.clear()


market_repository = MarketRepository()