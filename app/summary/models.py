"""
Daily Financial Summary models.
"""

from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel


class SummarySection(BaseModel):
    title: str
    content: str


class DailySummary(BaseModel):
    generated_at: datetime

    financial_health: str

    sections: List[SummarySection] = []

    recommendations: List[str] = []

    closing_message: str