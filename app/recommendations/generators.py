"""
Recommendation generators.
"""

from __future__ import annotations

from typing import List

from app.goals.models import GoalAnalysis
from app.health.models import HealthResponse
from app.insights.models import InsightResponse

from .models import (
    Recommendation,
    RecommendationCategory,
    RecommendationPriority,
)


class RecommendationGenerator:

    def generate(
        self,
        health: HealthResponse,
        insights: InsightResponse,
        goals: List[GoalAnalysis],
    ) -> List[Recommendation]:

        recommendations = []

        if health.score.overall < 60:

            recommendations.append(

                Recommendation(
                    title="Improve Financial Health",
                    description="Your overall financial health score is below the recommended level.",
                    action="Increase savings and reduce debt.",
                    category=RecommendationCategory.SAVINGS,
                    priority=RecommendationPriority.CRITICAL,
                    impact_score=100,
                )
            )

        for insight in insights.insights:

            recommendations.append(

                Recommendation(
                    title=insight.title,
                    description=insight.description,
                    action=insight.recommendation,
                    category=RecommendationCategory.SAVINGS,
                    priority=RecommendationPriority.HIGH,
                    impact_score=insight.score,
                )
            )

        for goal in goals:

            if not goal.on_track:

                recommendations.append(

                    Recommendation(
                        title=f"Goal: {goal.goal.name}",
                        description="This goal is behind schedule.",
                        action="Increase monthly contribution.",
                        category=RecommendationCategory.GOAL,
                        priority=RecommendationPriority.HIGH,
                        impact_score=95,
                    )
                )

        return recommendations