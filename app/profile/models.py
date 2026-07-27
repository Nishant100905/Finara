"""
Unified User Financial Profile.
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class Holding(BaseModel):
    symbol: str
    quantity: float
    average_price: float


class Liability(BaseModel):
    name: str
    outstanding_amount: float
    monthly_emi: float
    interest_rate: float


class UserFinancialProfile(BaseModel):
    """
    Master financial profile used throughout the application.
    """

    user_id: str

    monthly_income: float = Field(ge=0)

    monthly_expenses: float = Field(ge=0)

    monthly_savings: float = Field(ge=0)

    emergency_fund: float = Field(default=0, ge=0)

    investment_value: float = Field(default=0, ge=0)

    monthly_emi: float = Field(default=0, ge=0)

    risk_profile: str = "Moderate"

    investment_horizon: str = "Long Term"

    financial_goal: str | None = None

    preferred_currency: str = "INR"

    holdings: List[Holding] = []

    liabilities: List[Liability] = []

    watchlist: List[str] = []