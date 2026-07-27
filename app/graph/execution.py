"""
Execution Router
"""

from __future__ import annotations

from app.graph.state import GraphState


def next_agent(
    state: GraphState,
) -> str:

    plan = state.get(
        "execution_plan",
        [],
    )

    if not plan:
        return "end"

    completed = state.setdefault(
        "completed_agents",
        [],
    )

    for agent in plan:

        if agent not in completed:

            state["current_agent"] = agent

            completed.append(agent)

            return agent

    return "reflection"