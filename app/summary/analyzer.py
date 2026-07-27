"""
Summary Analyzer.
"""

from __future__ import annotations

from app.goals.models import GoalAnalysis
from app.health.models import HealthResponse
from app.insights.models import InsightResponse

from .generators import SummaryGenerator
from .models import DailySummary
from .priority import SummaryPrioritizer


class SummaryAnalyzer:

    @staticmethod
    def analyze(
        health: HealthResponse,
        insights: InsightResponse,
        goals: list[GoalAnalysis],
    ) -> DailySummary:

        summary = SummaryGenerator.generate(
            health=health,
            insights=insights,
            goals=goals,
        )

        summary.sections = SummaryPrioritizer.prioritize(
            summary.sections
        )

        return summary