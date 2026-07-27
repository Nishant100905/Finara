"""
Persistent financial profile operations.
"""

from __future__ import annotations

from app.memory.manager import memory


class ProfileService:
    """
    Handles user financial profile.
    """

    def get_profile(self):

        return memory.profile

    def update_income(self, income: float):

        memory.profile.income = income

    def update_expenses(self, expenses: float):

        memory.profile.expenses = expenses

    def update_savings(self, savings: float):

        memory.profile.savings = savings

    def update_goal(self, goal: str):

        memory.profile.investment_goal = goal

    def update_risk(self, risk: str):

        memory.profile.risk_tolerance = risk

    def update_time_horizon(
        self,
        horizon: str,
    ):

        memory.profile.time_horizon = horizon

    def add_asset(
        self,
        asset: str,
    ):

        if asset not in memory.profile.preferred_assets:
            memory.profile.preferred_assets.append(asset)


profile_service = ProfileService()