"""
Financial Forecasting Service.
"""

from __future__ import annotations

from datetime import date

from .analyzer import forecast_analyzer
from .goals import goal_forecast_engine
from .models import (
    ForecastResponse,
    ForecastResult,
    ForecastType,
)
from .projections import projection_engine
from .prompts import build_forecast_prompt
from .retirement import retirement_engine
from .scenarios import scenario_engine


class ForecastService:
    """
    Main forecasting service.
    """

    def forecast(
        self,
        profile: dict,
        portfolio: dict | None = None,
        goals: list | None = None,
    ) -> ForecastResponse:

        portfolio = portfolio or {}

        goals = goals or []

        analysis = forecast_analyzer.analyze(
            profile=profile,
            portfolio=portfolio,
            goals=goals,
        )

        cash_flow = projection_engine.cash_flow_projection(
            monthly_income=analysis["monthly_income"],
            monthly_expenses=analysis["monthly_expenses"],
        )

        net_worth = projection_engine.net_worth_projection(
            current_assets=(
                analysis["investment_value"]
                + analysis["current_savings"]
            ),
            current_liabilities=analysis["total_debt"],
            yearly_investment=(
                analysis["monthly_surplus"] * 12
            ),
        )

        retirement = retirement_engine.calculate(

            current_age=profile.get(
                "age",
                25,
            ),

            retirement_age=profile.get(
                "retirement_age",
                60,
            ),

            current_investments=analysis[
                "investment_value"
            ],

            monthly_investment=analysis[
                "monthly_surplus"
            ],

        )

        goal_results = []

        for goal in goals:

            goal_results.append(

                goal_forecast_engine.project(

                    goal_name=goal.get(
                        "name",
                        "Goal",
                    ),

                    target_amount=goal.get(
                        "target_amount",
                        0,
                    ),

                    current_amount=goal.get(
                        "current_amount",
                        0,
                    ),

                    monthly_contribution=goal.get(
                        "monthly_contribution",
                        0,
                    ),

                )

            )

        scenarios = scenario_engine.compare_sip(

            current_investment=analysis[
                "investment_value"
            ],

            monthly_sip=analysis[
                "monthly_surplus"
            ],

            extra_sip=1000,

        )

        prompt = build_forecast_prompt(

            profile=profile,

            analysis=analysis,

            forecast=net_worth,

            retirement=retirement,

            goals=goal_results,

            scenarios=scenarios,

        )

        summary = (
            f"Forecast generated. "
            f"Financial Health: "
            f"{forecast_analyzer.financial_health(analysis)}."
        )

        return ForecastResponse(

            generated_at=date.today(),

            result=ForecastResult(

                forecast_type=ForecastType.NET_WORTH,

                summary=summary,

                confidence=85,

            ),

            cash_flow=cash_flow,

            net_worth=net_worth,

            retirement=retirement,

            goals=goal_results,

            scenarios=scenarios,

        )

    def prompt(
        self,
        profile: dict,
        portfolio: dict | None = None,
        goals: list | None = None,
    ) -> str:

        portfolio = portfolio or {}

        goals = goals or []

        analysis = forecast_analyzer.analyze(
            profile,
            portfolio,
            goals,
        )

        return build_forecast_prompt(

            profile=profile,

            analysis=analysis,

            forecast=None,

            retirement=None,

            goals=goals,

            scenarios=None,

        )


forecast_service = ForecastService()