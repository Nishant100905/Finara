"""
Application-wide constants.

These values are shared across the project and
should never be hardcoded inside modules.
"""

from enum import Enum


# ----------------------------------------------------
# Intent Types
# ----------------------------------------------------

class Intent(str, Enum):
    RAG = "RAG"
    FINANCIAL = "FINANCIAL"
    HYBRID = "HYBRID"


# ----------------------------------------------------
# User Risk Profile
# ----------------------------------------------------

class RiskProfile(str, Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"


# ----------------------------------------------------
# Currency
# ----------------------------------------------------

DEFAULT_CURRENCY = "INR"


# ----------------------------------------------------
# Financial Defaults
# ----------------------------------------------------

DEFAULT_MONTHLY_INCOME = 0.0
DEFAULT_MONTHLY_EXPENSE = 0.0
DEFAULT_MONTHLY_SAVINGS = 0.0


# ----------------------------------------------------
# Memory
# ----------------------------------------------------

MAX_MEMORY_MESSAGES = 20
SUMMARY_TRIGGER = 25


# ----------------------------------------------------
# Retrieval
# ----------------------------------------------------

DEFAULT_TOP_K = 10
DEFAULT_RERANK_TOP_K = 5


# ----------------------------------------------------
# Cache
# ----------------------------------------------------

CACHE_TTL = 3600


# ----------------------------------------------------
# Retry
# ----------------------------------------------------

MAX_RETRIES = 3


# ----------------------------------------------------
# Confidence
# ----------------------------------------------------

INTENT_CONFIDENCE_THRESHOLD = 0.70