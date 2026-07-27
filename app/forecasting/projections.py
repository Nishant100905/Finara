"""
Financial projection engine.
"""

from __future__ import annotations

from .models import (
    CashFlowProjection,
    NetWorthProjection,
)


class ProjectionEngine:
    """
    Generates financial projections.
    """

    def cash_flow_projection(
        self,
        monthly_income: float,
        monthly_expenses: float,
        years: int = 5,
        annual_income_growth: float = 0.08,
        annual_expense_growth: float = 0.06,
    ) -> list[CashFlowProjection]:

        projections: list[
            CashFlowProjection
        ] = []

        income = monthly_income
        expenses = monthly_expenses

        for month in range(
            1,
            years * 12 + 1,
        ):

            if month % 12 == 1 and month > 1:

                income *= (
                    1 + annual_income_growth
                )

                expenses *= (
                    1 + annual_expense_growth
                )

            projections.append(

                CashFlowProjection(

                    month=month,

                    projected_income=round(
                        income,
                        2,
                    ),

                    projected_expenses=round(
                        expenses,
                        2,
                    ),

                    projected_savings=round(
                        income - expenses,
                        2,
                    ),

                )

            )

        return projections

    def net_worth_projection(
        self,
        current_assets: float,
        current_liabilities: float,
        yearly_investment: float,
        years: int = 20,
        annual_return: float = 0.12,
    ) -> list[NetWorthProjection]:

        projections: list[
            NetWorthProjection
        ] = []

        assets = current_assets

        liabilities = current_liabilities

        for year in range(
            1,
            years + 1,
        ):

            assets = (

                assets
                * (1 + annual_return)

            ) + yearly_investment

            net = assets - liabilities

            projections.append(

                NetWorthProjection(

                    year=year,

                    assets=round(
                        assets,
                        2,
                    ),

                    liabilities=round(
                        liabilities,
                        2,
                    ),

                    net_worth=round(
                        net,
                        2,
                    ),

                )

            )

        return projections


projection_engine = ProjectionEngine()