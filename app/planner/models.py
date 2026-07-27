"""
Pydantic models for the Financial Planner.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class PlanPriority(str, Enum):
    """
    Priority levels for action items.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class StrategyType(str, Enum):
    """
    Overall financial strategy.
    """

    EMERGENCY_FUND = "emergency_fund"
    DEBT_REDUCTION = "debt_reduction"
    BALANCED_GROWTH = "balanced_growth"
    AGGRESSIVE_INVESTING = "aggressive_investing"
    RETIREMENT = "retirement"
    WEALTH_PRESERVATION = "wealth_preservation"


class ActionItem(BaseModel):
    """
    A single financial action.
    """

    title: str
    description: str

    priority: PlanPriority

    category: str

    estimated_amount: Optional[float] = None

    due_date: Optional[date] = None

    completed: bool = False


class MonthlyPlan(BaseModel):
    """
    Monthly financial plan.
    """

    month: int

    title: str

    actions: list[ActionItem] = Field(default_factory=list)

    expected_savings: float = 0

    expected_investment: float = 0


class Milestone(BaseModel):
    """
    Financial milestone.
    """

    title: str

    target_amount: float

    current_amount: float = 0

    progress: float = 0

    expected_completion: Optional[date] = None


class FinancialRoadmap(BaseModel):
    """
    Multi-month roadmap.
    """

    months: list[MonthlyPlan] = Field(default_factory=list)

    milestones: list[Milestone] = Field(default_factory=list)


class FinancialPlan(BaseModel):
    """
    Complete financial plan.
    """

    strategy: StrategyType

    summary: str

    emergency_fund_target: float = 0

    monthly_savings_target: float = 0

    monthly_investment_target: float = 0

    debt_payment_target: float = 0

    roadmap: FinancialRoadmap


class SimulationResult(BaseModel):
    """
    Financial simulation output.
    """

    scenario: str

    projected_net_worth: float

    projected_savings: float

    projected_investment: float

    goal_completion_months: Optional[int] = None

    notes: str


class PlannerResponse(BaseModel):
    """
    Final planner response.
    """

    generated_at: date

    plan: FinancialPlan

    recommendations: list[str] = Field(default_factory=list)

    warnings: list[str] = Field(default_factory=list)

    simulations: list[SimulationResult] = Field(default_factory=list)