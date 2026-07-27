"""
General financial calculator tools.
"""

from langchain_core.tools import tool


@tool
def percentage(value: float, percent: float) -> float:
    """
    Calculate percentage of a value.

    Example:
    percentage(2000,10)=200
    """
    return round((value * percent) / 100, 2)


@tool
def compound_interest(
    principal: float,
    annual_rate: float,
    years: float,
    compounds_per_year: int = 12,
) -> float:
    """
    Calculate compound interest.

    annual_rate is in percentage.
    """

    r = annual_rate / 100

    amount = principal * (1 + r / compounds_per_year) ** (
        compounds_per_year * years
    )

    return round(amount, 2)


@tool
def simple_interest(
    principal: float,
    annual_rate: float,
    years: float,
) -> float:
    """
    Calculate simple interest.
    """

    interest = (principal * annual_rate * years) / 100

    return round(principal + interest, 2)


@tool
def profit_loss(
    cost_price: float,
    selling_price: float,
) -> dict:
    """
    Calculate profit or loss.
    """

    difference = selling_price - cost_price

    percentage_change = (difference / cost_price) * 100

    return {
        "profit_loss": round(difference, 2),
        "percentage": round(percentage_change, 2),
    }


@tool
def future_value(
    present_value: float,
    annual_growth: float,
    years: float,
) -> float:
    """
    Calculate future value after annual growth.
    """

    fv = present_value * ((1 + annual_growth / 100) ** years)

    return round(fv, 2)