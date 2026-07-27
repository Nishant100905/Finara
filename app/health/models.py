"""
Financial Health models.
"""

from __future__ import annotations

from pydantic import BaseModel


class HealthScore(BaseModel):

    savings: int

    emergency: int

    debt: int

    investment: int

    cashflow: int

    overall: int


class HealthResponse(BaseModel):

    score: HealthScore

    summary: str