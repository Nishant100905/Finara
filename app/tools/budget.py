"""
Budget planning tools.
"""

from langchain_core.tools import tool


@tool
def analyze_budget(
    monthly_income: float,
    rent: float,
    food: float,
    transport: float,
    shopping: float,
    entertainment: float,
    other: float,
) -> dict:
    """
    Analyze monthly budget.
    """

    total_expense = (
        rent
        + food
        + transport
        + shopping
        + entertainment
        + other
    )

    savings = monthly_income - total_expense

    savings_rate = (savings / monthly_income) * 100

    if savings_rate >= 30:
        status = "Excellent"

    elif savings_rate >= 20:
        status = "Good"

    elif savings_rate >= 10:
        status = "Average"

    else:
        status = "Poor"

    return {
        "income": monthly_income,
        "expenses": total_expense,
        "monthly_savings": round(savings, 2),
        "savings_rate": round(savings_rate, 2),
        "budget_health": status,
    }


@tool
def fifty_thirty_twenty_rule(
    monthly_income: float,
) -> dict:
    """
    Calculate 50/30/20 budget recommendation.
    """

    return {
        "needs": round(monthly_income * 0.50, 2),
        "wants": round(monthly_income * 0.30, 2),
        "savings": round(monthly_income * 0.20, 2),
    }