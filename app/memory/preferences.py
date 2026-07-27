"""
User preference service.
"""

from __future__ import annotations

from app.memory.manager import memory


class PreferenceService:

    def set_risk(
        self,
        risk: str,
    ):

        memory.profile.risk_tolerance = risk

    def set_goal(
        self,
        goal: str,
    ):

        memory.profile.investment_goal = goal

    def set_assets(
        self,
        assets: list[str],
    ):

        memory.profile.preferred_assets = assets

    def set_horizon(
        self,
        horizon: str,
    ):

        memory.profile.time_horizon = horizon

    def preferences(self):

        return {
            "risk": memory.profile.risk_tolerance,
            "goal": memory.profile.investment_goal,
            "assets": memory.profile.preferred_assets,
            "time_horizon": memory.profile.time_horizon,
        }


preferences = PreferenceService()