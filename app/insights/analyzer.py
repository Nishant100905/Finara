"""
Financial Insights Analyzer.

Coordinates rule execution, prioritization,
and response generation.
"""

from __future__ import annotations

from .generators import InsightGenerator
from .models import FinancialProfile, InsightResponse
from .priority import InsightPrioritizer


class FinancialInsightAnalyzer:
    """
    Main analysis engine.
    """

    def __init__(self):
        self.generator = InsightGenerator()
        self.prioritizer = InsightPrioritizer()

    def analyze(
        self,
        profile: FinancialProfile,
    ) -> InsightResponse:
        """
        Generate financial insights.
        """

        insights = self.generator.generate(profile)

        insights = self.prioritizer.prioritize(insights)

        return InsightResponse(
            insights=insights,
            total=len(insights),
        )