"""
Recommendation Service.
"""

from __future__ import annotations

from typing import List

from app.goals.models import GoalAnalysis
from app.health.models import HealthResponse
from app.insights.models import InsightResponse

from .analyzer import RecommendationAnalyzer
from .models import RecommendationResponse


class RecommendationService:

    def generate(
        self,
        health: HealthResponse,
        insights: InsightResponse,
        goals: List[GoalAnalysis],
    ) -> RecommendationResponse:

        return RecommendationAnalyzer.analyze(
            health=health,
            insights=insights,
            goals=goals,
        )


recommendations_service = RecommendationService()
recommendation_service = recommendations_service