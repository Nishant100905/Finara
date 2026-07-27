"""
Retirement forecasting engine.
"""

from __future__ import annotations

from .models import (
    RetirementProjection,
)


class RetirementEngine:
    """
    Retirement planner.
    """

    def calculate(
        self,
        current_age: int,
        retirement_age: int,
        current_investments: float,
        monthly_investment: float,
        expected_return: float = 0.12,
        inflation: float = 0.06,
        withdrawal_rate: float = 0.04,
    ) -> RetirementProjection:

        years = retirement_age - current_age

        corpus = current_investments

        monthly_return = (
            expected_return / 12
        )

        for _ in range(years * 12):

            corpus = (

                corpus
                * (1 + monthly_return)

            ) + monthly_investment

        annual_income = (
            corpus
            * withdrawal_rate
        )

        monthly_income = (
            annual_income / 12
        )

        inflation_factor = (
            (1 + inflation)
            ** years
        )

        target_corpus = (

            monthly_income
            * 12
            * 25
            * inflation_factor

        )

        return RetirementProjection(

            retirement_age=retirement_age,

            target_corpus=round(
                target_corpus,
                2,
            ),

            projected_corpus=round(
                corpus,
                2,
            ),

            monthly_income_after_retirement=round(
                monthly_income,
                2,
            ),

        )

    def fire_number(
        self,
        annual_expenses: float,
    ) -> float:
        """
        Calculate FIRE corpus.
        """

        return round(

            annual_expenses * 25,

            2,

        )

    def years_to_retirement(
        self,
        current_age: int,
        retirement_age: int,
    ) -> int:

        return max(

            retirement_age - current_age,

            0,

        )


retirement_engine = RetirementEngine()