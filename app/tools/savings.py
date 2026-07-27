"""
Savings planning tools.
"""

from math import ceil

from langchain_core.tools import tool


@tool
def savings_goal(
    goal_amount: float,
    current_savings: float,
    months: int,
) -> dict:
    """
    Calculate monthly savings required.
    """

    remaining = max(goal_amount - current_savings, 0)

    monthly = remaining / months

    weekly = monthly / 4

    daily = monthly / 30

    return {
        "goal": goal_amount,
        "current_savings": current_savings,
        "remaining": round(remaining, 2),
        "monthly_required": round(monthly, 2),
        "weekly_required": round(weekly, 2),
        "daily_required": round(daily, 2),
    }


@tool
def time_to_goal(
    goal_amount: float,
    current_savings: float,
    monthly_contribution: float,
) -> dict:
    """
    Estimate months required to achieve a savings goal.
    """

    remaining = max(goal_amount - current_savings, 0)

    if monthly_contribution <= 0:
        return {
            "error": "Monthly contribution must be greater than zero."
        }

    months = ceil(remaining / monthly_contribution)

    return {
        "remaining": round(remaining, 2),
        "estimated_months": months,
    }