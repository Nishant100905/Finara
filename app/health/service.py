"""
Health Service.
"""

from __future__ import annotations

from app.insights.models import FinancialProfile

from .analyzer import HealthAnalyzer


class HealthService:

    def analyze(
        self,
        profile: FinancialProfile,
    ):

        return HealthAnalyzer.analyze(profile)


health_service = HealthService()