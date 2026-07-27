"""
Goal planning engine.
"""

from __future__ import annotations

from datetime import date
from math import ceil

from .calculator import GoalCalculator
from .models import Goal


class GoalPlanner:
    """
    Generates financial plans for achieving goals.
    """

    @staticmethod
    def required_monthly_saving(goal: Goal):

        if goal.target_date is None:
            return None

        today = date.today()

        days = (goal.target_date - today).days

        if days <= 0:
            return None

        months = max(days / 30, 1)

        remaining = GoalCalculator.remaining_amount(goal)

        return round(remaining / months, 2)

    @staticmethod
    def will_reach_goal(goal: Goal):

        if goal.target_date is None:
            return True

        remaining_months = GoalCalculator.months_remaining(goal)

        if remaining_months is None:
            return False

        available_months = ceil(
            (goal.target_date - date.today()).days / 30
        )

        return remaining_months <= available_months

    @staticmethod
    def saving_gap(goal: Goal):

        required = GoalPlanner.required_monthly_saving(goal)

        if required is None:
            return None

        return round(
            required - goal.monthly_contribution,
            2,
        )