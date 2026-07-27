"""
Mutual fund helper tools.
"""

from langchain_core.tools import tool


@tool
def evaluate_mutual_fund(
    expense_ratio: float,
    annual_return: float,
    fund_age: int,
    alpha: float,
) -> dict:
    """
    Evaluate a mutual fund using simple metrics.
    """

    score = 0

    if expense_ratio < 1:
        score += 25

    if annual_return > 12:
        score += 25

    if fund_age >= 5:
        score += 25

    if alpha > 0:
        score += 25

    if score >= 90:
        rating = "Excellent"

    elif score >= 70:
        rating = "Good"

    elif score >= 50:
        rating = "Average"

    else:
        rating = "Weak"

    return {
        "score": score,
        "rating": rating,
    }


@tool
def lump_sum_projection(
    investment: float,
    annual_return: float,
    years: int,
) -> dict:
    """
    Project lump-sum investment growth.
    """

    future = investment * ((1 + annual_return / 100) ** years)

    return {
        "investment": investment,
        "future_value": round(future, 2),
        "profit": round(future - investment, 2),
    }