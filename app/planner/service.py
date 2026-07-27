"""
Financial planner service.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from .analyzer import financial_analyzer
from .milestones import milestone_manager
from .models import PlannerResponse
from .roadmap import roadmap_generator
from .simulator import financial_simulator
from .strategy import strategy_engine


class FinancialPlannerService:
    """
    Main financial planning service.
    """

    def create_plan(
        self,
        profile: dict[str, Any],
        goals: list[dict] | None = None,
        health: dict | None = None,
        insights: list[str] | None = None,
        recommendations: list[str] | None = None,
        portfolio: dict | None = None,
    ) -> PlannerResponse:
        """
        Create a complete financial plan.
        """

        plan = financial_analyzer.analyze(
            profile=profile,
            goals=goals,
            health=health,
            insights=insights,
            recommendations=recommendations,
            portfolio=portfolio,
        )

        actions = strategy_engine.generate_actions(
            plan
        )

        roadmap = roadmap_generator.build(
            plan
        )

        roadmap.milestones = (
            milestone_manager.generate(
                plan
            )
        )

        plan.roadmap = roadmap

        simulation = (
            financial_simulator.simulate(
                plan
            )
        )

        return PlannerResponse(
            generated_at=date.today(),
            plan=plan,
            recommendations=[
                action.title
                for action in actions
            ],
            warnings=self._warnings(
                profile,
            ),
            simulations=[
                simulation
            ],
        )

    def _warnings(
        self,
        profile: dict,
    ) -> list[str]:

        warnings = []

        income = float(
            profile.get(
                "monthly_income",
                0,
            )
        )

        expenses = float(
            profile.get(
                "monthly_expenses",
                0,
            )
        )

        debt = float(
            profile.get(
                "total_debt",
                0,
            )
        )

        emergency = float(
            profile.get(
                "emergency_fund",
                0,
            )
        )

        if expenses > income:

            warnings.append(
                "Monthly expenses exceed monthly income."
            )

        if debt > income * 6:

            warnings.append(
                "Debt level is significantly high."
            )

        if emergency < expenses * 3:

            warnings.append(
                "Emergency fund is below the recommended level."
            )

        return warnings


financial_planner_service = FinancialPlannerService()

# Backward compatibility
planner_service = financial_planner_service