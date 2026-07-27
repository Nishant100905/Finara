"""
Summary prioritization.
"""

from __future__ import annotations

from .models import SummarySection


class SummaryPrioritizer:
    """
    Prioritizes important sections.
    """

    PRIORITY_ORDER = {
        "Financial Health": 1,
        "Critical Alert": 2,
        "Top Insight": 3,
        "Goal Progress": 4,
        "Portfolio": 5,
        "Market": 6,
        "Recommendations": 7,
    }

    @classmethod
    def prioritize(
        cls,
        sections: list[SummarySection],
    ) -> list[SummarySection]:

        return sorted(
            sections,
            key=lambda section: cls.PRIORITY_ORDER.get(
                section.title,
                999,
            ),
        )