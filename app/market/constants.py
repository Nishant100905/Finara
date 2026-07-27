"""
Market module constants.
"""

DEFAULT_PROVIDER = "yahoo"

DEFAULT_CURRENCY = "INR"

CACHE_TTL = 300  # 5 minutes

REQUEST_TIMEOUT = 10

MAX_BATCH_SIZE = 100

SUPPORTED_ASSETS = {
    "STOCK",
    "ETF",
    "INDEX",
    "CRYPTO",
    "MUTUAL_FUND",
}