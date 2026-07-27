"""
Financial milestone manager.
"""

from __future__ import annotations

from datetime import date, timedelta

from .models import (
    FinancialPlan,
    Milestone,
)


class MilestoneManager:
    """
    Generates financial milestones and tracks progress.
    """

    def generate(
        self,
        plan: FinancialPlan,
    ) -> list[Milestone]:

        today = date.today()

        milestones = [

            Milestone(
                title="Emergency Fund",
                target_amount=plan.emergency_fund_target,
                current_amount=0,
                progress=0,
                expected_completion=today + timedelta(days=180),
            ),

            Milestone(
                title="Annual Savings",
                target_amount=plan.monthly_savings_target * 12,
                current_amount=0,
                progress=0,
                expected_completion=today + timedelta(days=365),
            ),

            Milestone(
                title="Annual Investments",
                target_amount=plan.monthly_investment_target * 12,
                current_amount=0,
                progress=0,
                expected_completion=today + timedelta(days=365),
            ),

        ]

        return milestones

    def update_progress(
        self,
        milestone: Milestone,
        current_amount: float,
    ) -> Milestone:

        milestone.current_amount = current_amount

        if milestone.target_amount > 0:

            milestone.progress = round(

                (
                    current_amount
                    / milestone.target_amount
                )
                * 100,

                2,

            )

        else:

            milestone.progress = 0

        return milestone

    def completed(
        self,
        milestone: Milestone,
    ) -> bool:

        return (
            milestone.current_amount
            >= milestone.target_amount
        )


milestone_manager = MilestoneManager()