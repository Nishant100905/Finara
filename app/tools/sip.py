"""
Systematic Investment Plan (SIP) tools.
"""

from math import pow

from langchain_core.tools import tool


@tool
def sip_maturity(
    monthly_investment: float,
    annual_return: float,
    years: int,
) -> dict:
    """
    Calculate SIP maturity amount.
    """

    monthly_rate = annual_return / 12 / 100
    months = years * 12

    if monthly_rate == 0:
        maturity = monthly_investment * months
    else:
        maturity = (
            monthly_investment
            * (
                (pow(1 + monthly_rate, months) - 1)
                / monthly_rate
            )
            * (1 + monthly_rate)
        )

    invested = monthly_investment * months

    return {
        "monthly_investment": monthly_investment,
        "invested_amount": round(invested, 2),
        "estimated_value": round(maturity, 2),
        "estimated_returns": round(maturity - invested, 2),
    }


@tool
def required_sip(
    target_amount: float,
    annual_return: float,
    years: int,
) -> dict:
    """
    Calculate required SIP for a target amount.
    """

    monthly_rate = annual_return / 12 / 100
    months = years * 12

    if monthly_rate == 0:
        sip = target_amount / months
    else:
        sip = target_amount / (
            ((pow(1 + monthly_rate, months) - 1) / monthly_rate)
            * (1 + monthly_rate)
        )

    return {
        "target_amount": target_amount,
        "required_monthly_sip": round(sip, 2),
    }