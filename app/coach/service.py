"""
Financial Coach service.
"""

from __future__ import annotations

from .analyzer import financial_coach_analyzer
from .insights import insight_generator
from .models import CoachResponse
from .nudges import nudge_generator
from .prompts import build_coach_prompt
from .rules import coach_rules


class FinancialCoachService:
    """
    Main Financial Coach service.
    """

    def coach(
        self,
        profile: dict,
        goals: list | None = None,
        portfolio: dict | None = None,
        health: dict | None = None,
    ) -> CoachResponse:
        """
        Generate a complete coaching response.
        """

        goals = goals or []
        portfolio = portfolio or {}
        health = health or {}

        alerts, advice = (
            financial_coach_analyzer.analyze(
                profile=profile,
                goals=goals,
                portfolio=portfolio,
                health=health,
            )
        )

        rule_alerts = coach_rules.evaluate(
            profile
        )

        alerts.extend(rule_alerts)

        nudges = nudge_generator.generate(
            profile
        )

        insights = insight_generator.generate(
            profile=profile,
            health=health,
            portfolio=portfolio,
            goals=goals,
        )

        advice.extend(insights)

        prompt = build_coach_prompt(
            profile=profile,
            alerts=alerts,
            advice=advice,
            nudges=nudges,
            insights=insights,
        )

        return CoachResponse(
            alerts=alerts,
            advice=advice,
            nudges=nudges,
            daily_summary=None,
            weekly_summary=None,
        )

    def prompt(
        self,
        profile: dict,
        goals: list,
        portfolio: dict,
        health: dict,
    ) -> str:
        """
        Return only the AI coaching prompt.
        """

        alerts, advice = (
            financial_coach_analyzer.analyze(
                profile,
                goals,
                portfolio,
                health,
            )
        )

        nudges = nudge_generator.generate(
            profile
        )

        insights = insight_generator.generate(
            profile,
            health,
            portfolio,
            goals,
        )

        return build_coach_prompt(
            profile=profile,
            alerts=alerts,
            advice=advice,
            nudges=nudges,
            insights=insights,
        )

financial_coach_service = FinancialCoachService()

# Backward compatibility
coach_service = financial_coach_service