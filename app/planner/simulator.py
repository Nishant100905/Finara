"""
Financial forecasting simulator.
"""

from __future__ import annotations

from .models import (
    FinancialPlan,
    SimulationResult,
)


class FinancialSimulator:
    """
    Simulates future financial outcomes.
    """

    def simulate(
        self,
        plan: FinancialPlan,
        years: int = 5,
        annual_return: float = 0.12,
    ) -> SimulationResult:

        investment = 0.0

        savings = 0.0

        monthly_return = annual_return / 12

        months = years * 12

        for _ in range(months):

            investment = (

                investment
                * (1 + monthly_return)

            ) + plan.monthly_investment_target

            savings += plan.monthly_savings_target

        projected_net_worth = (

            investment
            + savings

        )

        return SimulationResult(

            scenario=f"{years}-Year Projection",

            projected_net_worth=round(
                projected_net_worth,
                2,
            ),

            projected_savings=round(
                savings,
                2,
            ),

            projected_investment=round(
                investment,
                2,
            ),

            goal_completion_months=self._estimate_goal_completion(
                plan
            ),

            notes=(
                "Projection assumes consistent monthly "
                "contributions and fixed annual return."
            ),

        )

    def compare_sip(
        self,
        plan: FinancialPlan,
        extra_monthly_investment: float,
        years: int = 10,
        annual_return: float = 0.12,
    ) -> SimulationResult:

        investment = 0.0

        monthly_return = annual_return / 12

        monthly = (

            plan.monthly_investment_target
            + extra_monthly_investment

        )

        for _ in range(years * 12):

            investment = (

                investment
                * (1 + monthly_return)

            ) + monthly

        return SimulationResult(

            scenario=(
                f"SIP + ₹{extra_monthly_investment:,.0f}"
            ),

            projected_net_worth=round(
                investment,
                2,
            ),

            projected_savings=0,

            projected_investment=round(
                investment,
                2,
            ),

            goal_completion_months=None,

            notes=(
                "Simulation with increased monthly investment."
            ),

        )

    def _estimate_goal_completion(
        self,
        plan: FinancialPlan,
    ) -> int | None:

        target = plan.emergency_fund_target

        monthly = plan.monthly_savings_target

        if monthly <= 0:

            return None

        return int(target / monthly)


financial_simulator = FinancialSimulator()