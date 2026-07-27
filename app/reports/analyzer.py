"""
Collect information from every financial module.
"""

from __future__ import annotations

from typing import Any


class ReportAnalyzer:
    """
    Aggregates all financial information into
    a report-ready structure.
    """

    def analyze(
        self,
        profile: dict[str, Any],
        health: dict | None = None,
        goals: list | None = None,
        planner: dict | None = None,
        recommendations: list | None = None,
        forecast: dict | None = None,
        coach: dict | None = None,
        market: dict | None = None,
        portfolio: dict | None = None,
    ) -> dict[str, Any]:

        return {

            "profile": profile,

            "health": health or {},

            "goals": goals or [],

            "planner": planner or {},

            "recommendations": recommendations or [],

            "forecast": forecast or {},

            "coach": coach or {},

            "market": market or {},

            "portfolio": portfolio or {},

        }

    def build_statistics(
        self,
        report_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build useful report statistics.
        """

        profile = report_data.get(
            "profile",
            {},
        )

        goals = report_data.get(
            "goals",
            [],
        )

        portfolio = report_data.get(
            "portfolio",
            {},
        )

        monthly_income = profile.get(
            "monthly_income",
            0,
        )

        monthly_expenses = profile.get(
            "monthly_expenses",
            0,
        )

        savings = max(
            monthly_income - monthly_expenses,
            0,
        )

        return {

            "monthly_income": monthly_income,

            "monthly_expenses": monthly_expenses,

            "monthly_savings": savings,

            "goal_count": len(goals),

            "portfolio_value": portfolio.get(
                "total_value",
                0,
            ),

            "health_score": report_data.get(
                "health",
                {},
            ).get(
                "score",
                0,
            ),

        }

    def executive_summary(
        self,
        report_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build a preliminary executive summary.
        AI will later refine this.
        """

        stats = self.build_statistics(
            report_data,
        )

        return {

            "overview": (
                "Financial report generated successfully."
            ),

            "strengths": [

                (
                    "Positive monthly savings."
                    if stats["monthly_savings"] > 0
                    else "Income requires improvement."
                )

            ],

            "risks": [

                (
                    "Emergency fund should be reviewed."
                )

            ],

            "opportunities": [

                (
                    "Increase monthly investments."
                )

            ],

            "recommendations": [

                (
                    "Track expenses regularly."
                ),

                (
                    "Review portfolio quarterly."
                ),

            ],

        }


report_analyzer = ReportAnalyzer()