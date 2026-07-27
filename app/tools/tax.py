"""
Tax calculation tools.
"""

from langchain_core.tools import tool


@tool
def income_tax_old_regime(
    annual_income: float,
) -> dict:
    """
    Estimate Indian income tax under the old regime.
    (Simplified calculation. Does not include cess or rebates.)
    """

    tax = 0

    if annual_income <= 250000:
        tax = 0

    elif annual_income <= 500000:
        tax = (annual_income - 250000) * 0.05

    elif annual_income <= 1000000:
        tax = (
            12500
            + (annual_income - 500000) * 0.20
        )

    else:
        tax = (
            112500
            + (annual_income - 1000000) * 0.30
        )

    return {
        "regime": "Old",
        "annual_income": annual_income,
        "estimated_tax": round(tax, 2),
        "effective_rate": round((tax / annual_income) * 100, 2)
        if annual_income
        else 0,
    }


@tool
def income_tax_new_regime(
    annual_income: float,
) -> dict:
    """
    Simplified new regime calculation.
    (Educational purposes only.)
    """

    slabs = [
        (400000, 0),
        (800000, 0.05),
        (1200000, 0.10),
        (1600000, 0.15),
        (2000000, 0.20),
        (2400000, 0.25),
    ]

    tax = 0
    previous = 0

    for limit, rate in slabs:

        if annual_income > limit:
            tax += (limit - previous) * rate
            previous = limit

        else:
            tax += (annual_income - previous) * rate
            return {
                "regime": "New",
                "annual_income": annual_income,
                "estimated_tax": round(tax, 2),
            }

    tax += (annual_income - 2400000) * 0.30

    return {
        "regime": "New",
        "annual_income": annual_income,
        "estimated_tax": round(tax, 2),
    }


@tool
def compare_tax_regimes(
    annual_income: float,
) -> dict:
    """
    Compare estimated tax under old and new regimes.
    """

    old_tax = income_tax_old_regime.invoke(
        {"annual_income": annual_income}
    )["estimated_tax"]

    new_tax = income_tax_new_regime.invoke(
        {"annual_income": annual_income}
    )["estimated_tax"]

    better = "Old" if old_tax < new_tax else "New"

    return {
        "old_regime_tax": old_tax,
        "new_regime_tax": new_tax,
        "recommended_regime": better,
    }