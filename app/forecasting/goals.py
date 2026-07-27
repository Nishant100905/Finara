"""
Goal forecasting engine.
"""

from __future__ import annotations

from datetime import date, timedelta

from .models import GoalProjection


class GoalForecastEngine:
    """
    Forecast financial goal completion.
    """

    def project(
        self,
        goal_name: str,
        target_amount: float,
        current_amount: float,
        monthly_contribution: float,
        annual_return: float = 0.10,
    ) -> GoalProjection:

        balance = current_amount

        monthly_return = annual_return / 12

        months = 0

        while balance < target_amount and months < 600:

            balance = (
                balance * (1 + monthly_return)
            ) + monthly_contribution

            months += 1

        completion = (
            date.today()
            + timedelta(days=months * 30)
        )

        return GoalProjection(

            goal_name=goal_name,

            target_amount=round(
                target_amount,
                2,
            ),

            current_amount=round(
                current_amount,
                2,
            ),

            monthly_contribution=round(
                monthly_contribution,
                2,
            ),

            estimated_completion_date=completion,

            months_remaining=months,

        )

    def emergency_fund_goal(
        self,
        monthly_expenses: float,
        current_savings: float,
        monthly_savings: float,
    ) -> GoalProjection:

        target = monthly_expenses * 6

        return self.project(

            goal_name="Emergency Fund",

            target_amount=target,

            current_amount=current_savings,

            monthly_contribution=monthly_savings,

        )


goal_forecast_engine = GoalForecastEngine()