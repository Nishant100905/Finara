"""
Public service for Financial Insights.
"""

from __future__ import annotations

from .analyzer import FinancialInsightAnalyzer
from .models import FinancialProfile, InsightResponse


class InsightService:
    """
    Entry point used by agents and APIs.
    """

    def __init__(self):
        self.analyzer = FinancialInsightAnalyzer()

    def generate(
        self,
        profile: FinancialProfile,
    ) -> InsightResponse:
        """
        Generate ranked financial insights.
        """

        return self.analyzer.analyze(profile)


# Singleton instance
insight_service = InsightService()