"""
Financial nudges generator.
"""

from __future__ import annotations

from .models import (
    AdviceCategory,
    FinancialNudge,
)


class NudgeGenerator:
    """
    Generates proactive financial nudges.
    """

    def generate(
        self,
        profile: dict,
    ) -> list[FinancialNudge]:

        nudges: list[FinancialNudge] = []

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

        surplus = max(
            income - expenses,
            0,
        )

        if surplus > 0:

            nudges.append(

                FinancialNudge(

                    message=(
                        f"You have approximately "
                        f"₹{surplus:,.0f} available "
                        "this month. Consider investing "
                        "part of it."
                    ),

                    category=AdviceCategory.INVESTMENT,

                )

            )

        if emergency < expenses * 6:

            nudges.append(

                FinancialNudge(

                    message=(
                        "Building a six-month emergency "
                        "fund should be one of your "
                        "highest priorities."
                    ),

                    category=AdviceCategory.SAVINGS,

                )

            )

        nudges.append(

            FinancialNudge(

                message=(
                    "Review your subscriptions this "
                    "month and cancel any you no "
                    "longer use."
                ),

                category=AdviceCategory.BUDGET,

            )

        )

        nudges.append(

            FinancialNudge(

                message=(
                    "Review your investment portfolio "
                    "at least once every quarter."
                ),

                category=AdviceCategory.INVESTMENT,

            )

        )

        nudges.append(

            FinancialNudge(

                message=(
                    "Track every expense for the next "
                    "seven days to identify spending "
                    "patterns."
                ),

                category=AdviceCategory.BUDGET,

            )

        )

        return nudges


nudge_generator = NudgeGenerator()