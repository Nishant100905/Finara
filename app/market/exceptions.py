"""
Market module exceptions.
"""


class MarketException(Exception):
    """Base market exception."""


class SymbolNotFoundError(MarketException):
    """Symbol not found."""


class ProviderUnavailableError(MarketException):
    """Market provider unavailable."""


class InvalidMarketDataError(MarketException):
    """Invalid market response."""


class CacheError(MarketException):
    """Cache operation failed."""