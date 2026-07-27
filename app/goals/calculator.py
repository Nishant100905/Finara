"""
Goal planning calculations.
"""

from __future__ import annotations

from datetime import date, timedelta
from math import ceil

from .models import Goal, GoalProgress


class GoalCalculator:
    """
    Performs financial goal calculations.
    """

    @staticmethod
    def completion_percentage(goal: Goal) -> float:

        if goal.target_amount <= 0:
            return 0.0

        percentage = (
            goal.current_amount
            / goal.target_amount
        ) * 100

        return round(min(percentage, 100), 2)

    @staticmethod
    def remaining_amount(goal: Goal) -> float:

        return max(
            goal.target_amount - goal.current_amount,
            0,
        )

    @staticmethod
    def months_remaining(goal: Goal):

        if goal.monthly_contribution <= 0:
            return None

        remaining = GoalCalculator.remaining_amount(goal)

        return ceil(
            remaining / goal.monthly_contribution
        )

    @staticmethod
    def estimated_completion(goal: Goal):

        months = GoalCalculator.months_remaining(goal)

        if months is None:
            return None

        return date.today() + timedelta(days=months * 30)

    @staticmethod
    def analyze(goal: Goal) -> GoalProgress:

        return GoalProgress(
            percentage=GoalCalculator.completion_percentage(goal),
            remaining_amount=GoalCalculator.remaining_amount(goal),
            months_remaining=GoalCalculator.months_remaining(goal),
            estimated_completion_date=GoalCalculator.estimated_completion(goal),
        )