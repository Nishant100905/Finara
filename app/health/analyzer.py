"""
Financial Health Analyzer.
"""

from __future__ import annotations

from app.insights.models import FinancialProfile

from .models import (
    HealthResponse,
    HealthScore,
)


class HealthAnalyzer:

    @staticmethod
    def analyze(
        profile: FinancialProfile,
    ) -> HealthResponse:

        savings = min(
            int(
                (
                    profile.monthly_savings
                    / max(profile.monthly_income, 1)
                )
                * 500
            ),
            100,
        )

        emergency = min(
            int(
                (
                    profile.emergency_fund
                    / max(profile.monthly_expenses * 6, 1)
                )
                * 100
            ),
            100,
        )

        debt = max(
            100
            - int(
                (
                    profile.monthly_emi
                    / max(profile.monthly_income, 1)
                )
                * 100
            ),
            0,
        )

        investment = 100 if profile.investment_value > 0 else 40

        cashflow = (
            100
            if profile.monthly_income >= profile.monthly_expenses
            else 40
        )

        overall = int(
            (
                savings
                + emergency
                + debt
                + investment
                + cashflow
            )
            / 5
        )

        summary = (
            "Excellent"
            if overall >= 80
            else "Good"
            if overall >= 60
            else "Needs Improvement"
        )

        return HealthResponse(
            score=HealthScore(
                savings=savings,
                emergency=emergency,
                debt=debt,
                investment=investment,
                cashflow=cashflow,
                overall=overall,
            ),
            summary=summary,
        )