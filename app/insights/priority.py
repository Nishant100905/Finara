"""
Insight prioritization utilities.
"""

from __future__ import annotations

from typing import List

from .models import Insight


class InsightPrioritizer:
    """
    Ranks insights by priority.
    """

    def prioritize(
        self,
        insights: List[Insight],
    ) -> List[Insight]:

        unique = {}

        for insight in insights:

            key = (
                insight.title,
                insight.category,
            )

            if key not in unique:
                unique[key] = insight

            elif insight.score > unique[key].score:
                unique[key] = insight

        ranked = sorted(
            unique.values(),
            key=lambda x: (
                x.score,
                x.severity.value,
            ),
            reverse=True,
        )

        return ranked

    def top(
        self,
        insights: List[Insight],
        limit: int = 5,
    ) -> List[Insight]:

        return self.prioritize(insights)[:limit]