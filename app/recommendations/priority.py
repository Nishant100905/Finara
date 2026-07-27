"""
Recommendation prioritization.
"""

from __future__ import annotations

from .models import Recommendation


class RecommendationPrioritizer:
    """
    Removes duplicates and sorts recommendations.
    """

    @staticmethod
    def prioritize(
        recommendations: list[Recommendation],
    ) -> list[Recommendation]:

        unique: dict[str, Recommendation] = {}

        for recommendation in recommendations:

            key = recommendation.title.lower()

            existing = unique.get(key)

            if (
                existing is None
                or recommendation.impact_score > existing.impact_score
            ):
                unique[key] = recommendation

        return sorted(
            unique.values(),
            key=lambda recommendation: (
                recommendation.priority.value,
                recommendation.impact_score,
            ),
            reverse=True,
        )

    @staticmethod
    def top(
        recommendations: list[Recommendation],
        limit: int = 5,
    ) -> list[Recommendation]:

        return RecommendationPrioritizer.prioritize(
            recommendations
        )[:limit]