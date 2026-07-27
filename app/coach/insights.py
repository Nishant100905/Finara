"""
Financial insights generator.
"""

from __future__ import annotations

from .models import (
    AdviceCategory,
    CoachAdvice,
)


class InsightGenerator:
    """
    Generate high-level financial insights.
    """

    def generate(
        self,
        profile: dict,
        health: dict | None = None,
        portfolio: dict | None = None,
        goals: list | None = None,
    ) -> list[CoachAdvice]:

        insights: list[CoachAdvice] = []

        health = health or {}
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

        emergency = float(
            profile.get(
                "emergency_fund",
                0,
            )
        )

        debt = float(
            profile.get(
                "total_debt",
                0,
            )
        )

        savings_rate = 0

        if income > 0:

            savings_rate = (
                (
                    income - expenses
                )
                / income
            ) * 100

        if savings_rate >= 30:

            insights.append(

                CoachAdvice(

                    title="Excellent Savings Rate",

                    description=(
                        f"You save approximately "
                        f"{savings_rate:.1f}% "
                        "of your monthly income."
                    ),

                    category=AdviceCategory.SAVINGS,

                    priority=3,

                )

            )

        elif savings_rate < 10:

            insights.append(

                CoachAdvice(

                    title="Low Savings Rate",

                    description=(
                        "Consider reducing discretionary "
                        "expenses to increase savings."
                    ),

                    category=AdviceCategory.BUDGET,

                    priority=1,

                )

            )

        if emergency >= expenses * 6:

            insights.append(

                CoachAdvice(

                    title="Emergency Fund Healthy",

                    description=(
                        "Your emergency reserve "
                        "is well funded."
                    ),

                    category=AdviceCategory.SAVINGS,

                    priority=3,

                )

            )

        if debt == 0:

            insights.append(

                CoachAdvice(

                    title="Debt Free",

                    description=(
                        "Great job maintaining "
                        "zero outstanding debt."
                    ),

                    category=AdviceCategory.DEBT,

                    priority=3,

                )

            )

        score = health.get(
            "overall_score",
            0,
        )

        if score >= 80:

            insights.append(

                CoachAdvice(

                    title="Excellent Financial Health",

                    description=(
                        "Maintain your current "
                        "financial habits."
                    ),

                    category=AdviceCategory.GENERAL,

                    priority=2,

                )

            )

        elif score < 60:

            insights.append(

                CoachAdvice(

                    title="Financial Health Needs Improvement",

                    description=(
                        "Focus on budgeting, saving "
                        "and debt reduction."
                    ),

                    category=AdviceCategory.GENERAL,

                    priority=1,

                )

            )

        portfolio_value = portfolio.get(
            "total_value",
            0,
        )

        if portfolio_value:

            insights.append(

                CoachAdvice(

                    title="Portfolio Growth",

                    description=(
                        f"Current portfolio value "
                        f"is ₹{portfolio_value:,.2f}."
                    ),

                    category=AdviceCategory.INVESTMENT,

                    priority=2,

                )

            )

        if goals:

            insights.append(

                CoachAdvice(

                    title="Goal Tracking",

                    description=(
                        f"You currently have "
                        f"{len(goals)} active "
                        "financial goals."
                    ),

                    category=AdviceCategory.GOALS,

                    priority=2,

                )

            )

        return insights


insight_generator = InsightGenerator()