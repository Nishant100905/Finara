"""
Pydantic models for the Financial Insights Engine.
"""

from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class InsightCategory(str, Enum):
    SAVINGS = "Savings"
    EXPENSE = "Expense"
    INVESTMENT = "Investment"
    DEBT = "Debt"
    GOAL = "Goal"
    PORTFOLIO = "Portfolio"
    TAX = "Tax"
    CASHFLOW = "Cash Flow"


class Insight(BaseModel):
    """
    Represents one financial insight.
    """

    title: str

    description: str

    recommendation: str

    category: InsightCategory

    severity: Severity

    score: int = Field(
        default=50,
        ge=0,
        le=100,
        description="Priority score",
    )


class FinancialProfile(BaseModel):
    """
    Minimal profile required for analysis.
    """

    monthly_income: float = 0

    monthly_expenses: float = 0

    monthly_savings: float = 0

    emergency_fund: float = 0

    debt: float = 0

    monthly_emi: float = 0

    investment_value: float = 0

    risk_profile: str = "Moderate"


class InsightResponse(BaseModel):
    """
    Final response returned by analyzer.
    """

    insights: List[Insight] = []

    total: int = 0