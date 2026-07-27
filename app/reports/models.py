"""
Pydantic models for AI Financial Reports.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ReportType(str, Enum):
    """
    Supported report types.
    """

    FINANCIAL_HEALTH = "financial_health"
    PORTFOLIO = "portfolio"
    GOALS = "goals"
    RETIREMENT = "retirement"
    FORECAST = "forecast"
    MONTHLY = "monthly"
    COMPLETE = "complete"


class ReportSection(BaseModel):
    """
    Single report section.
    """

    title: str

    content: str

    order: int


class ExecutiveSummary(BaseModel):
    """
    AI generated executive summary.
    """

    overview: str

    strengths: list[str] = Field(default_factory=list)

    risks: list[str] = Field(default_factory=list)

    opportunities: list[str] = Field(default_factory=list)

    recommendations: list[str] = Field(default_factory=list)


class ReportMetadata(BaseModel):
    """
    Metadata.
    """

    generated_at: datetime

    report_type: ReportType

    generated_by: str = "Financial AI Advisor"

    version: str = "1.0.0"


class FinancialReport(BaseModel):
    """
    Complete report.
    """

    title: str

    generated_for: str

    report_date: date

    metadata: ReportMetadata

    executive_summary: ExecutiveSummary

    sections: list[
        ReportSection
    ] = Field(default_factory=list)

    raw_data: dict[str, Any] = Field(default_factory=dict)


class ReportResponse(BaseModel):
    """
    API response.
    """

    report: FinancialReport

    markdown: str | None = None

    pdf_path: str | None = None

    excel_path: str | None = None