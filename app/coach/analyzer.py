"""
Financial Coach analyzer.
"""

from __future__ import annotations

from typing import Any

from .models import (
    AdviceCategory,
    AlertLevel,
    CoachAdvice,
    FinancialAlert,
)


class FinancialCoachAnalyzer:
    """
    Analyze financial behaviour and generate
    alerts and coaching advice.
    """

    def analyze(
        self,
        profile: dict[str, Any],
        goals: list[dict] | None = None,
        portfolio: dict | None = None,
        health: dict | None = None,
    ) -> tuple[
        list[FinancialAlert],
        list[CoachAdvice],
    ]:

        alerts: list[FinancialAlert] = []

        advice: list[CoachAdvice] = []

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

        if expenses > income:

            alerts.append(

                FinancialAlert(

                    title="Overspending",

                    message=(
                        "Your monthly expenses "
                        "are higher than your income."
                    ),

                    level=AlertLevel.CRITICAL,

                    category=AdviceCategory.BUDGET,

                )

            )

        if emergency < expenses * 3:

            alerts.append(

                FinancialAlert(

                    title="Emergency Fund Low",

                    message=(
                        "Increase your emergency "
                        "fund to at least "
                        "3 months of expenses."
                    ),

                    level=AlertLevel.WARNING,

                    category=AdviceCategory.SAVINGS,

                )

            )

        if debt > income * 6:

            advice.append(

                CoachAdvice(

                    title="Prioritize Debt",

                    description=(
                        "Focus on paying off "
                        "high-interest debt "
                        "before increasing investments."
                    ),

                    category=AdviceCategory.DEBT,

                    priority=1,

                    action="Increase monthly debt repayment",

                )

            )

        if income > expenses:

            advice.append(

                CoachAdvice(

                    title="Invest Monthly Surplus",

                    description=(
                        "Allocate part of your "
                        "monthly surplus toward "
                        "long-term investments."
                    ),

                    category=AdviceCategory.INVESTMENT,

                    priority=2,

                    action="Start or increase SIP",

                )

            )

        if goals:

            advice.append(

                CoachAdvice(

                    title="Track Goal Progress",

                    description=(
                        "Review your financial "
                        "goals every month and "
                        "adjust contributions."
                    ),

                    category=AdviceCategory.GOALS,

                    priority=3,

                    action="Review goals",

                )

            )

        return alerts, advice


financial_coach_analyzer = (
    FinancialCoachAnalyzer()
)