"""
Forecast input analyzer.
"""

from __future__ import annotations

from typing import Any


class ForecastAnalyzer:
    """
    Analyze user financial profile before forecasting.
    """

    def analyze(
        self,
        profile: dict[str, Any],
        portfolio: dict | None = None,
        goals: list | None = None,
    ) -> dict:

        portfolio = portfolio or {}

        goals = goals or []

        income = float(
            profile.get(
                "monthly_income",
                0,
            )
        )

        expenses = float(
            profile.get(
                "monthly_expenses",
                0,
            )
        )

        savings = float(
            profile.get(
                "emergency_fund",
                0,
            )
        )

        investments = float(
            portfolio.get(
                "total_value",
                0,
            )
        )

        debt = float(
            profile.get(
                "total_debt",
                0,
            )
        )

        surplus = max(
            income - expenses,
            0,
        )

        savings_rate = 0

        if income > 0:

            savings_rate = (
                surplus
                / income
            ) * 100

        return {

            "monthly_income": income,

            "monthly_expenses": expenses,

            "monthly_surplus": surplus,

            "savings_rate": round(
                savings_rate,
                2,
            ),

            "current_savings": savings,

            "investment_value": investments,

            "total_debt": debt,

            "goal_count": len(goals),

        }

    def financial_health(
        self,
        analysis: dict,
    ) -> str:

        score = 0

        if analysis["savings_rate"] >= 30:

            score += 40

        elif analysis["savings_rate"] >= 20:

            score += 30

        elif analysis["savings_rate"] >= 10:

            score += 20

        if analysis["total_debt"] == 0:

            score += 30

        elif analysis["total_debt"] < (
            analysis["monthly_income"] * 6
        ):

            score += 20

        if analysis["investment_value"] > 0:

            score += 30

        if score >= 80:

            return "Excellent"

        if score >= 60:

            return "Good"

        if score >= 40:

            return "Average"

        return "Needs Improvement"


forecast_analyzer = ForecastAnalyzer()