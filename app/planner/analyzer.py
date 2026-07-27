"""
Financial profile analyzer.
"""

from __future__ import annotations

from typing import Any

from .models import FinancialPlan, FinancialRoadmap, StrategyType


class FinancialAnalyzer:
    """
    Analyze a user's financial profile and determine
    the appropriate planning strategy.
    """

    def analyze(
        self,
        profile: dict[str, Any],
        goals: list[dict] | None = None,
        health: dict[str, Any] | None = None,
        insights: list[str] | None = None,
        recommendations: list[str] | None = None,
        portfolio: dict[str, Any] | None = None,
    ) -> FinancialPlan:
        """
        Generate a base financial plan from user data.
        """

        goals = goals or []
        health = health or {}
        insights = insights or []
        recommendations = recommendations or []
        portfolio = portfolio or {}

        monthly_income = float(
            profile.get("monthly_income", 0)
        )

        monthly_expenses = float(
            profile.get("monthly_expenses", 0)
        )

        debt = float(
            profile.get("total_debt", 0)
        )

        emergency_fund = float(
            profile.get("emergency_fund", 0)
        )

        monthly_surplus = max(
            monthly_income - monthly_expenses,
            0,
        )

        strategy = self._determine_strategy(
            debt=debt,
            emergency_fund=emergency_fund,
            monthly_income=monthly_income,
            monthly_surplus=monthly_surplus,
        )

        emergency_target = monthly_expenses * 6

        monthly_savings = monthly_surplus * 0.40

        monthly_investment = monthly_surplus * 0.60

        debt_payment = min(
            debt,
            monthly_surplus * 0.50,
        )

        summary = self._generate_summary(
            strategy,
            monthly_surplus,
            debt,
            emergency_target,
        )

        return FinancialPlan(
            strategy=strategy,
            summary=summary,
            emergency_fund_target=round(
                emergency_target,
                2,
            ),
            monthly_savings_target=round(
                monthly_savings,
                2,
            ),
            monthly_investment_target=round(
                monthly_investment,
                2,
            ),
            debt_payment_target=round(
                debt_payment,
                2,
            ),
            roadmap=FinancialRoadmap(),
        )

    def _determine_strategy(
        self,
        *,
        debt: float,
        emergency_fund: float,
        monthly_income: float,
        monthly_surplus: float,
    ) -> StrategyType:
        """
        Decide the overall financial strategy.
        """

        if debt > monthly_income * 6:
            return StrategyType.DEBT_REDUCTION

        if emergency_fund < monthly_income * 3:
            return StrategyType.EMERGENCY_FUND

        if monthly_surplus >= monthly_income * 0.40:
            return StrategyType.AGGRESSIVE_INVESTING

        if monthly_surplus >= monthly_income * 0.20:
            return StrategyType.BALANCED_GROWTH

        return StrategyType.WEALTH_PRESERVATION

    def _generate_summary(
        self,
        strategy: StrategyType,
        monthly_surplus: float,
        debt: float,
        emergency_target: float,
    ) -> str:
        """
        Generate a concise financial summary.
        """

        return (
            f"Recommended strategy: {strategy.value.replace('_', ' ').title()}. "
            f"Monthly surplus: ₹{monthly_surplus:,.2f}. "
            f"Outstanding debt: ₹{debt:,.2f}. "
            f"Emergency fund target: ₹{emergency_target:,.2f}."
        )


financial_analyzer = FinancialAnalyzer()