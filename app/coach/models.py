"""
Pydantic models for the Financial Coach.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class AlertLevel(str, Enum):
    """
    Alert severity.
    """

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    CRITICAL = "critical"


class AdviceCategory(str, Enum):
    """
    Categories of coaching advice.
    """

    BUDGET = "budget"
    SAVINGS = "savings"
    INVESTMENT = "investment"
    DEBT = "debt"
    GOALS = "goals"
    INSURANCE = "insurance"
    TAX = "tax"
    MARKET = "market"
    GENERAL = "general"


class FinancialAlert(BaseModel):
    """
    High priority alert.
    """

    title: str

    message: str

    level: AlertLevel

    category: AdviceCategory

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )


class CoachAdvice(BaseModel):
    """
    Personalized coaching advice.
    """

    title: str

    description: str

    category: AdviceCategory

    priority: int = 1

    action: Optional[str] = None


class FinancialNudge(BaseModel):
    """
    Small proactive reminder.
    """

    message: str

    category: AdviceCategory

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )


class DailySummary(BaseModel):
    """
    Daily coaching summary.
    """

    summary: str

    highlights: list[str] = Field(
        default_factory=list
    )


class WeeklySummary(BaseModel):
    """
    Weekly coaching summary.
    """

    summary: str

    achievements: list[str] = Field(
        default_factory=list
    )

    improvements: list[str] = Field(
        default_factory=list
    )


class CoachResponse(BaseModel):
    """
    Complete coach response.
    """

    alerts: list[FinancialAlert] = Field(
        default_factory=list
    )

    advice: list[CoachAdvice] = Field(
        default_factory=list
    )

    nudges: list[FinancialNudge] = Field(
        default_factory=list
    )

    daily_summary: Optional[DailySummary] = None

    weekly_summary: Optional[
        WeeklySummary
    ] = None