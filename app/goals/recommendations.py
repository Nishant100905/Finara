"""
Goal recommendation engine.
"""

from __future__ import annotations

from typing import List

from .calculator import GoalCalculator
from .models import (
    Goal,
    GoalPriority,
    GoalRecommendation,
)
from .planner import GoalPlanner


class GoalRecommendationEngine:

    @staticmethod
    def generate(
        goal: Goal,
    ) -> List[GoalRecommendation]:

        recommendations = []

        gap = GoalPlanner.saving_gap(goal)

        if gap is not None:

            if gap > 0:

                recommendations.append(
                    GoalRecommendation(
                        title="Increase Savings",
                        message=f"Increase monthly savings by ₹{gap:,.0f} to stay on track.",
                        priority=GoalPriority.HIGH,
                    )
                )

            elif gap < 0:

                recommendations.append(
                    GoalRecommendation(
                        title="Excellent Progress",
                        message="You are saving more than required.",
                        priority=GoalPriority.LOW,
                    )
                )

        if not GoalPlanner.will_reach_goal(goal):

            recommendations.append(
                GoalRecommendation(
                    title="Goal Delay",
                    message="At your current savings rate, you may miss your target date.",
                    priority=GoalPriority.CRITICAL,
                )
            )

        progress = GoalCalculator.completion_percentage(goal)

        if progress >= 75:

            recommendations.append(
                GoalRecommendation(
                    title="Almost There",
                    message="You're close to achieving this goal.",
                    priority=GoalPriority.LOW,
                )
            )

        elif progress < 25:

            recommendations.append(
                GoalRecommendation(
                    title="Increase Contributions",
                    message="Consider increasing monthly savings.",
                    priority=GoalPriority.MEDIUM,
                )
            )

        if goal.monthly_contribution == 0:

            recommendations.append(
                GoalRecommendation(
                    title="Contribution Missing",
                    message="No monthly contribution has been set.",
                    priority=GoalPriority.CRITICAL,
                )
            )

        return recommendations