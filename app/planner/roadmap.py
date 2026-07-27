"""
Financial roadmap generator.
"""

from __future__ import annotations

from .models import (
    FinancialPlan,
    FinancialRoadmap,
    MonthlyPlan,
)
from .strategy import strategy_engine


class RoadmapGenerator:
    """
    Builds a month-by-month roadmap.
    """

    def build(
        self,
        plan: FinancialPlan,
        months: int = 12,
    ) -> FinancialRoadmap:

        actions = strategy_engine.generate_actions(
            plan
        )

        roadmap = FinancialRoadmap()

        for month in range(
            1,
            months + 1,
        ):

            roadmap.months.append(

                MonthlyPlan(

                    month=month,

                    title=f"Month {month}",

                    actions=actions,

                    expected_savings=plan.monthly_savings_target,

                    expected_investment=plan.monthly_investment_target,

                )

            )

        roadmap.milestones = self._build_milestones(
            plan
        )

        return roadmap

    def _build_milestones(
        self,
        plan: FinancialPlan,
    ):

        milestones = []

        milestones.append(
            {
                "title": "Emergency Fund",
                "target_amount": plan.emergency_fund_target,
                "current_amount": 0,
                "progress": 0,
            }
        )

        milestones.append(
            {
                "title": "Monthly Savings Habit",
                "target_amount": plan.monthly_savings_target * 12,
                "current_amount": 0,
                "progress": 0,
            }
        )

        milestones.append(
            {
                "title": "Investment Target",
                "target_amount": plan.monthly_investment_target * 12,
                "current_amount": 0,
                "progress": 0,
            }
        )

        return milestones


roadmap_generator = RoadmapGenerator()