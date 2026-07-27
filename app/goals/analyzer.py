"""
Goal analysis engine.
"""

from __future__ import annotations

from .calculator import GoalCalculator
from .models import Goal, GoalAnalysis
from .planner import GoalPlanner
from .recommendations import GoalRecommendationEngine


class GoalAnalyzer:

    @staticmethod
    def analyze(
        goal: Goal,
    ) -> GoalAnalysis:

        return GoalAnalysis(
            goal=goal,
            progress=GoalCalculator.analyze(goal),
            required_monthly_saving=GoalPlanner.required_monthly_saving(goal),
            on_track=GoalPlanner.will_reach_goal(goal),
            recommendations=GoalRecommendationEngine.generate(goal),
        )