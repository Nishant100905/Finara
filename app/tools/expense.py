"""
Expense analysis tools.
"""

from langchain_core.tools import tool


@tool
def analyze_expenses(
    food: float,
    rent: float,
    transport: float,
    shopping: float,
    entertainment: float,
    healthcare: float,
    utilities: float,
    others: float,
) -> dict:
    """
    Analyze expense distribution.
    """

    expenses = {
        "Food": food,
        "Rent": rent,
        "Transport": transport,
        "Shopping": shopping,
        "Entertainment": entertainment,
        "Healthcare": healthcare,
        "Utilities": utilities,
        "Others": others,
    }

    total = sum(expenses.values())

    percentages = {
        category: round((amount / total) * 100, 2) if total else 0
        for category, amount in expenses.items()
    }

    highest = max(expenses, key=expenses.get)

    return {
        "total_expenses": round(total, 2),
        "category_breakdown": expenses,
        "percentage_breakdown": percentages,
        "highest_spending_category": highest,
    }


@tool
def detect_overspending(
    monthly_income: float,
    total_expenses: float,
) -> dict:
    """
    Detect whether spending is healthy.
    """

    ratio = (total_expenses / monthly_income) * 100

    if ratio <= 60:
        status = "Healthy"

    elif ratio <= 80:
        status = "Watch Spending"

    elif ratio <= 100:
        status = "High Spending"

    else:
        status = "Overspending"

    return {
        "expense_ratio": round(ratio, 2),
        "status": status,
    }