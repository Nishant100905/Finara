"""
Pydantic models for Financial Forecasting.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ForecastType(str, Enum):
    """
    Types of forecasts.
    """

    CASH_FLOW = "cash_flow"
    NET_WORTH = "net_worth"
    RETIREMENT = "retirement"
    GOAL = "goal"
    INVESTMENT = "investment"


class CashFlowProjection(BaseModel):
    """
    Monthly cash flow projection.
    """

    month: int

    projected_income: float

    projected_expenses: float

    projected_savings: float


class NetWorthProjection(BaseModel):
    """
    Net worth projection.
    """

    year: int

    assets: float

    liabilities: float

    net_worth: float


class RetirementProjection(BaseModel):
    """
    Retirement forecast.
    """

    retirement_age: int

    target_corpus: float

    projected_corpus: float

    monthly_income_after_retirement: float


class GoalProjection(BaseModel):
    """
    Goal completion forecast.
    """

    goal_name: str

    target_amount: float

    current_amount: float

    monthly_contribution: float

    estimated_completion_date: Optional[date] = None

    months_remaining: Optional[int] = None


class ScenarioComparison(BaseModel):
    """
    Compare two scenarios.
    """

    scenario_name: str

    projected_net_worth: float

    projected_corpus: float

    goal_completion_months: int


class ForecastResult(BaseModel):
    """
    Complete forecast result.
    """

    forecast_type: ForecastType

    summary: str

    confidence: float = Field(
        ge=0,
        le=100,
    )


class ForecastResponse(BaseModel):
    """
    Main forecasting response.
    """

    generated_at: date

    result: ForecastResult

    cash_flow: list[
        CashFlowProjection
    ] = Field(default_factory=list)

    net_worth: list[
        NetWorthProjection
    ] = Field(default_factory=list)

    retirement: Optional[
        RetirementProjection
    ] = None

    goals: list[
        GoalProjection
    ] = Field(default_factory=list)

    scenarios: list[
        ScenarioComparison
    ] = Field(default_factory=list)