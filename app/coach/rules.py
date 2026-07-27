"""
Business rules for the Financial Coach.
"""

from __future__ import annotations

from .models import (
    AdviceCategory,
    AlertLevel,
    FinancialAlert,
)


class CoachRules:
    """
    Rule engine for financial coaching.
    """

    def evaluate(
        self,
        profile: dict,
    ) -> list[FinancialAlert]:

        alerts: list[FinancialAlert] = []

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

        debt = float(
            profile.get(
                "total_debt",
                0,
            )
        )

        if income <= 0:

            alerts.append(

                FinancialAlert(

                    title="Income Missing",

                    message=(
                        "Income information is "
                        "required for accurate coaching."
                    ),

                    level=AlertLevel.WARNING,

                    category=AdviceCategory.GENERAL,

                )

            )

        if expenses > income:

            alerts.append(

                FinancialAlert(

                    title="Overspending",

                    message=(
                        "Your expenses are greater "
                        "than your monthly income."
                    ),

                    level=AlertLevel.CRITICAL,

                    category=AdviceCategory.BUDGET,

                )

            )

        if savings < expenses * 3:

            alerts.append(

                FinancialAlert(

                    title="Emergency Fund",

                    message=(
                        "Your emergency fund is "
                        "below the recommended level."
                    ),

                    level=AlertLevel.WARNING,

                    category=AdviceCategory.SAVINGS,

                )

            )

        if debt > income * 6:

            alerts.append(

                FinancialAlert(

                    title="High Debt",

                    message=(
                        "Your debt is significantly "
                        "higher than your income."
                    ),

                    level=AlertLevel.CRITICAL,

                    category=AdviceCategory.DEBT,

                )

            )

        if income > 0 and expenses <= income * 0.5:

            alerts.append(

                FinancialAlert(

                    title="Healthy Spending",

                    message=(
                        "Excellent! Your spending "
                        "is well under control."
                    ),

                    level=AlertLevel.SUCCESS,

                    category=AdviceCategory.BUDGET,

                )

            )

        return alerts


coach_rules = CoachRules()