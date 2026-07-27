"""
Company name to ticker symbol resolver.
"""

from __future__ import annotations

import logging

from .service import market_service
from .yahoo import YahooFinanceService

logger = logging.getLogger(__name__)


class SymbolResolver:
    """
    Resolve company names into ticker symbols.
    """

    def __init__(self):

        self.yahoo = YahooFinanceService()

        self.common_symbols = {

            # US
            "apple": "AAPL",
            "microsoft": "MSFT",
            "google": "GOOGL",
            "alphabet": "GOOGL",
            "amazon": "AMZN",
            "tesla": "TSLA",
            "meta": "META",
            "nvidia": "NVDA",
            "netflix": "NFLX",

            # India
            "reliance": "RELIANCE.NS",
            "tcs": "TCS.NS",
            "infosys": "INFY.NS",
            "hdfc": "HDFCBANK.NS",
            "icici": "ICICIBANK.NS",
            "sbi": "SBIN.NS",
            "itc": "ITC.NS",
            "wipro": "WIPRO.NS",
            "lt": "LT.NS",
            "larsen and toubro": "LT.NS",
            "adani enterprises": "ADANIENT.NS",
            "adani ports": "ADANIPORTS.NS",
        }

    async def resolve(
        self,
        query: str,
    ) -> str:

        query = query.strip()

        if await market_service.validate(query):
            return query.upper()

        key = query.lower()

        if key in self.common_symbols:
            return self.common_symbols[key]

        results = await self.search(query)

        if not results:
            raise ValueError(
                f"No stock found for '{query}'."
            )

        return results[0]["symbol"]

    async def search(
        self,
        query: str,
    ) -> list[dict]:

        try:

            quotes = await self.yahoo.search(query)

            normalized = []

            for quote in quotes:

                symbol = quote.get("symbol")

                if not symbol:
                    continue

                normalized.append(

                    {

                        "symbol": symbol,

                        "name": (
                            quote.get("shortname")
                            or quote.get("longname")
                            or quote.get("name")
                        ),

                        "exchange": (
                            quote.get("exchDisp")
                            or quote.get("exchange")
                        ),

                        "type": (
                            quote.get("quoteType")
                            or quote.get("type")
                        ),

                    }

                )

            return normalized

        except Exception:

            logger.exception(
                "Failed to resolve %s",
                query,
            )

            return []

    async def suggest(
        self,
        query: str,
    ) -> list[str]:

        results = await self.search(query)

        names = [
            item["name"]
            for item in results[:5]
            if item.get("name")
        ]

        if names:
            return names

        # Fall back to fuzzy match against the built-in alias table
        # so that short partials like "Tes" still surface something.
        needle = query.lower()
        aliases = sorted(self.common_symbols.keys())
        for alias in aliases:
            if alias.startswith(needle):
                mapped = self.common_symbols[alias]
                return [f"{mapped} ({alias})"]

        return []

    def add_alias(
        self,
        name: str,
        symbol: str,
    ) -> None:

        self.common_symbols[
            name.lower()
        ] = symbol


symbol_resolver = SymbolResolver()