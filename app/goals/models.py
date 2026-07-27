"""
Goal models.

Represents user financial goals.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class GoalPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class GoalStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class GoalType(str, Enum):
    EMERGENCY_FUND = "Emergency Fund"
    RETIREMENT = "Retirement"
    HOUSE = "House"
    CAR = "Car"
    BIKE = "Bike"
    PHONE = "Phone"
    LAPTOP = "Laptop"
    WATCH = "Watch"
    VACATION = "Vacation"
    EDUCATION = "Education"
    CUSTOM = "Custom"


class Goal(BaseModel):
    """
    Financial Goal.
    """

    id: Optional[int] = None

    name: str

    goal_type: GoalType

    target_amount: float = Field(..., gt=0)

    current_amount: float = 0

    monthly_contribution: float = 0

    target_date: Optional[date] = None

    priority: GoalPriority = GoalPriority.MEDIUM

    status: GoalStatus = GoalStatus.NOT_STARTED


class GoalProgress(BaseModel):
    """
    Goal progress summary.
    """

    percentage: float

    remaining_amount: float

    months_remaining: Optional[float]

    estimated_completion_date: Optional[date]

from typing import List


class GoalRecommendation(BaseModel):
    """
    Structured recommendation.
    """

    title: str

    message: str

    priority: GoalPriority = GoalPriority.MEDIUM


class GoalAnalysis(BaseModel):
    """
    Complete Goal Analysis.
    """

    goal: Goal

    progress: GoalProgress

    required_monthly_saving: float | None = None

    on_track: bool

    recommendations: List[GoalRecommendation] = []