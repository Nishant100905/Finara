"""
Loan EMI calculator.
"""

from math import pow

from langchain_core.tools import tool


@tool
def calculate_emi(
    loan_amount: float,
    annual_interest: float,
    tenure_years: int,
) -> dict:
    """
    Calculate EMI for a loan.
    """

    monthly_rate = annual_interest / 12 / 100
    months = tenure_years * 12

    if monthly_rate == 0:
        emi = loan_amount / months
    else:
        emi = (
            loan_amount
            * monthly_rate
            * pow(1 + monthly_rate, months)
        ) / (
            pow(1 + monthly_rate, months) - 1
        )

    total_payment = emi * months

    interest_paid = total_payment - loan_amount

    return {
        "loan_amount": loan_amount,
        "monthly_emi": round(emi, 2),
        "total_interest": round(interest_paid, 2),
        "total_payment": round(total_payment, 2),
    }


@tool
def loan_affordability(
    monthly_income: float,
    monthly_emi: float,
) -> dict:
    """
    Check whether EMI is affordable.
    """

    ratio = (monthly_emi / monthly_income) * 100

    if ratio <= 30:
        status = "Excellent"

    elif ratio <= 40:
        status = "Acceptable"

    elif ratio <= 50:
        status = "Risky"

    else:
        status = "Not Recommended"

    return {
        "emi_income_ratio": round(ratio, 2),
        "affordability": status,
    }