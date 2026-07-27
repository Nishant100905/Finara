"""
Recommendation models.
"""

from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel


class RecommendationPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RecommendationCategory(str, Enum):
    SAVINGS = "Savings"
    INVESTMENT = "Investment"
    GOAL = "Goal"
    DEBT = "Debt"
    CASHFLOW = "Cash Flow"
    PORTFOLIO = "Portfolio"


class Recommendation(BaseModel):

    title: str

    description: str

    action: str

    priority: RecommendationPriority

    category: RecommendationCategory

    impact_score: int


class RecommendationResponse(BaseModel):

    recommendations: List[Recommendation] = []

    total: int = 0