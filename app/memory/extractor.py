"""
Memory Extractor

Extracts persistent user facts from conversations.
"""

from __future__ import annotations

import re
from typing import Any


class MemoryExtractor:
    """
    Extract structured facts from user messages.
    """

    INCOME_PATTERN = re.compile(
        r"(salary|income|earn)\D*([\d,]+)",
        re.IGNORECASE,
    )

    EXPENSE_PATTERN = re.compile(
        r"(expense|spend|expenses)\D*([\d,]+)",
        re.IGNORECASE,
    )

    def extract(self, message: str) -> dict[str, Any]:

        result: dict[str, Any] = {}

        income = self.INCOME_PATTERN.search(message)

        if income:
            value = income.group(2).replace(",", "")
            result["income"] = float(value)

        expenses = self.EXPENSE_PATTERN.search(message)

        if expenses:
            value = expenses.group(2).replace(",", "")
            result["expenses"] = float(value)

        lower = message.lower()

        # -----------------------------
        # Risk Tolerance
        # -----------------------------

        if "low risk" in lower:

            result["risk_tolerance"] = "Low"

        elif "medium risk" in lower:

            result["risk_tolerance"] = "Moderate"

        elif "high risk" in lower:

            result["risk_tolerance"] = "High"

        # -----------------------------
        # Goals
        # -----------------------------

        if "buy a house" in lower:

            result["investment_goal"] = "Buy House"

        elif "retirement" in lower:

            result["investment_goal"] = "Retirement"

        elif "financial freedom" in lower:

            result["investment_goal"] = "Financial Freedom"

        # -----------------------------
        # Assets
        # -----------------------------

        assets = []

        keywords = {
            "stocks": "Stocks",
            "mutual fund": "Mutual Funds",
            "mutual funds": "Mutual Funds",
            "sip": "SIP",
            "gold": "Gold",
            "etf": "ETF",
            "crypto": "Crypto",
            "bitcoin": "Bitcoin",
            "real estate": "Real Estate",
        }

        for key, value in keywords.items():

            if key in lower:
                assets.append(value)

        if assets:
            result["preferred_assets"] = list(set(assets))

        return result


extractor = MemoryExtractor()