"""
Daily Financial Summary Generator.
"""

from __future__ import annotations

from datetime import datetime

from app.goals.models import GoalAnalysis
from app.health.models import HealthResponse
from app.insights.models import InsightResponse

from .models import (
    DailySummary,
    SummarySection,
)


class SummaryGenerator:

    @staticmethod
    def generate(
        health: HealthResponse,
        insights: InsightResponse,
        goals: list[GoalAnalysis],
    ) -> DailySummary:

        sections: list[SummarySection] = []

        recommendations: list[str] = []

        sections.append(
            SummarySection(
                title="Financial Health",
                content=(
                    f"Your financial health score is "
                    f"{health.score.overall}/100 "
                    f"({health.summary})."
                ),
            )
        )

        if insights.insights:

            sections.append(
                SummarySection(
                    title="Top Insight",
                    content=insights.insights[0].description,
                )
            )

            recommendations.append(
                insights.insights[0].recommendation
            )

        delayed = [
            goal.goal.name
            for goal in goals
            if not goal.on_track
        ]

        if delayed:

            sections.append(
                SummarySection(
                    title="Goal Progress",
                    content=(
                        "These goals are behind schedule: "
                        + ", ".join(delayed)
                    ),
                )
            )

        return DailySummary(
            generated_at=datetime.utcnow(),
            financial_health=health.summary,
            sections=sections,
            recommendations=recommendations,
            closing_message=(
                "Keep following your financial plan. Small, consistent improvements compound over time."
            ),
        )