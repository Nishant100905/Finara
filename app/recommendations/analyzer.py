"""
Recommendation Analyzer.
"""

from __future__ import annotations

from typing import List

from app.goals.models import GoalAnalysis
from app.health.models import HealthResponse
from app.insights.models import InsightResponse

from .generators import RecommendationGenerator
from .models import RecommendationResponse
from .priority import RecommendationPrioritizer


class RecommendationAnalyzer:

    generator = RecommendationGenerator()

    @classmethod
    def analyze(
        cls,
        health: HealthResponse,
        insights: InsightResponse,
        goals: List[GoalAnalysis],
    ) -> RecommendationResponse:

        recommendations = cls.generator.generate(
            health=health,
            insights=insights,
            goals=goals,
        )

        recommendations = RecommendationPrioritizer.prioritize(
            recommendations
        )

        return RecommendationResponse(
            recommendations=recommendations,
            total=len(recommendations),
        )