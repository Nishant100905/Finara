"""
Goal Service.

Public entry point for Goal Management.
"""

from __future__ import annotations

from typing import List

from .analyzer import GoalAnalyzer
from .models import Goal


class GoalService:
    """
    High-level Goal API.
    """

    def analyze(self, goal: Goal):

        return GoalAnalyzer.analyze(goal)

    def analyze_many(
        self,
        goals: List[Goal],
    ):

        return [
            GoalAnalyzer.analyze(goal)
            for goal in goals
        ]


goal_service = GoalService()

# Backward compatibility
goals_service = goal_service