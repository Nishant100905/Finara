"""
Market Service.

Public interface for the Market module.
"""

from __future__ import annotations

from .models import (
    HistoricalPrice,
    QuoteResponse,
)
from .repository import market_repository


class MarketService:
    """
    High-level Market service.

    Controllers, AI agents, and tools should use this
    instead of calling the repository directly.
    """

    async def quote(
        self,
        symbol: str,
        *,
        refresh: bool = False,
    ) -> QuoteResponse:

        return await market_repository.get_quote(
            symbol,
            use_cache=not refresh,
        )

    async def history(
        self,
        symbol: str,
        period: str = "6mo",
    ) -> list[HistoricalPrice]:

        return await market_repository.get_history(
            symbol,
            period,
        )

    async def validate(
        self,
        symbol: str,
    ) -> bool:

        return await market_repository.validate_symbol(
            symbol,
        )

    def invalidate_cache(
        self,
        symbol: str,
    ) -> None:

        market_repository.invalidate_quote(symbol)

    def clear_cache(self) -> None:

        market_repository.clear_cache()


market_service = MarketService()