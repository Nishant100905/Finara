"""
Currency conversion tools.
"""

from langchain_core.tools import tool


EXCHANGE_RATES = {
    "INR": 1.0,
    "USD": 87.0,
    "EUR": 102.0,
    "GBP": 118.0,
    "JPY": 0.60,
    "AED": 23.7,
}


@tool
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
) -> dict:
    """
    Convert currency using static exchange rates.

    Later this can be replaced with a live exchange-rate API.
    """

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency not in EXCHANGE_RATES:
        return {"error": f"Unsupported currency: {from_currency}"}

    if to_currency not in EXCHANGE_RATES:
        return {"error": f"Unsupported currency: {to_currency}"}

    inr = amount * EXCHANGE_RATES[from_currency]

    converted = inr / EXCHANGE_RATES[to_currency]

    return {
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
        "converted_amount": round(converted, 2),
    }


@tool
def supported_currencies() -> list:
    """
    Return supported currencies.
    """

    return sorted(EXCHANGE_RATES.keys())