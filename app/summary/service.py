"""
Daily Summary Service.
"""

from __future__ import annotations

from app.goals.models import GoalAnalysis
from app.health.models import HealthResponse
from app.insights.models import InsightResponse

from .analyzer import SummaryAnalyzer
from .models import DailySummary


class SummaryService:

    def generate(
        self,
        health: HealthResponse,
        insights: InsightResponse,
        goals: list[GoalAnalysis],
    ) -> DailySummary:

        return SummaryAnalyzer.analyze(
            health=health,
            insights=insights,
            goals=goals,
        )


summary_service = SummaryService()