"""
Financial insight generator.

Runs every business rule and collects insights.
"""

from __future__ import annotations

from typing import List

from .models import FinancialProfile, Insight
from .rules import RULES


class InsightGenerator:
    """
    Executes all insight rules.
    """

    def generate(
        self,
        profile: FinancialProfile,
    ) -> List[Insight]:

        insights: List[Insight] = []

        for rule in RULES:

            try:
                result = rule(profile)

                if result:
                    insights.extend(result)

            except Exception:
                # One failing rule should never stop analysis.
                continue

        return insights