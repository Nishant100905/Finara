"""
Scenario comparison engine.
"""

from __future__ import annotations

from .models import ScenarioComparison


class ScenarioEngine:
    """
    Compare financial scenarios.
    """

    def compare_sip(
        self,
        current_investment: float,
        monthly_sip: float,
        extra_sip: float,
        years: int = 15,
        annual_return: float = 0.12,
    ) -> list[ScenarioComparison]:

        current = self._future_value(
            current_investment,
            monthly_sip,
            years,
            annual_return,
        )

        improved = self._future_value(
            current_investment,
            monthly_sip + extra_sip,
            years,
            annual_return,
        )

        return [

            ScenarioComparison(

                scenario_name="Current SIP",

                projected_net_worth=round(
                    current,
                    2,
                ),

                projected_corpus=round(
                    current,
                    2,
                ),

                goal_completion_months=years * 12,

            ),

            ScenarioComparison(

                scenario_name=f"SIP + ₹{extra_sip:,.0f}",

                projected_net_worth=round(
                    improved,
                    2,
                ),

                projected_corpus=round(
                    improved,
                    2,
                ),

                goal_completion_months=max(
                    years * 12 - 12,
                    0,
                ),

            ),

        ]

    def compare_retirement_age(
        self,
        corpus: float,
        monthly_investment: float,
        current_age: int,
        retirement_one: int,
        retirement_two: int,
        annual_return: float = 0.12,
    ) -> list[ScenarioComparison]:

        first = self._future_value(

            corpus,

            monthly_investment,

            retirement_one - current_age,

            annual_return,

        )

        second = self._future_value(

            corpus,

            monthly_investment,

            retirement_two - current_age,

            annual_return,

        )

        return [

            ScenarioComparison(

                scenario_name=f"Retire at {retirement_one}",

                projected_net_worth=round(
                    first,
                    2,
                ),

                projected_corpus=round(
                    first,
                    2,
                ),

                goal_completion_months=(
                    retirement_one
                    - current_age
                ) * 12,

            ),

            ScenarioComparison(

                scenario_name=f"Retire at {retirement_two}",

                projected_net_worth=round(
                    second,
                    2,
                ),

                projected_corpus=round(
                    second,
                    2,
                ),

                goal_completion_months=(
                    retirement_two
                    - current_age
                ) * 12,

            ),

        ]

    def _future_value(
        self,
        initial: float,
        monthly: float,
        years: int,
        annual_return: float,
    ) -> float:

        balance = initial

        monthly_return = annual_return / 12

        for _ in range(years * 12):

            balance = (

                balance
                * (1 + monthly_return)

            ) + monthly

        return balance


scenario_engine = ScenarioEngine()