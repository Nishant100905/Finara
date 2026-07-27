"""
Base provider interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .models import MarketData


class BaseMarketProvider(ABC):

    @abstractmethod
    async def get_quote(
        self,
        symbol: str,
    ) -> MarketData:
        ...

    @abstractmethod
    async def get_history(
        self,
        symbol: str,
        period: str = "1mo",
    ):
        ...
        