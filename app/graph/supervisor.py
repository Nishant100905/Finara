"""
Graph Supervisor.

Creates and manages execution plans for the graph.
"""

from __future__ import annotations

import logging

from app.graph.planner import planner
from app.graph.state import GraphState

logger = logging.getLogger(__name__)


class GraphSupervisor:
    """
    Supervises graph execution.

    Responsibilities:
    - Read classified intent
    - Build execution plan
    - Route to next agent
    """

    def create_plan(
        self,
        state: GraphState,
    ) -> GraphState:

        metadata = state.setdefault("metadata", {})

        intent = metadata.get(
            "intent",
            "rag",
        ).lower()

        query = state.get(
            "query",
            "",
        )

        plan = planner.create_plan(
            intent=intent,
            query=query,
        )

        plan_strings = [
            step.agent.value
            for step in plan.steps
        ]

        state["completed_agents"] = []

        metadata["execution_plan"] = plan

        logger.info(
            "Execution plan created: %s",
            plan_strings,
        )

        return {
            "execution_plan": plan_strings,
            "completed_agents": [],
            "metadata": metadata,
        }

    # -------------------------------------------------

    def route(
        self,
        state: GraphState,
    ) -> str:
        """
        Return the next agent to execute.
        """

        plan = state.get(
            "execution_plan",
            [],
        )

        completed = state.get(
            "completed_agents",
            [],
        )

        for agent in plan:

            if agent not in completed:

                completed.append(agent)

                state["completed_agents"] = completed

                state["current_agent"] = agent

                return agent

        return "reflection"


supervisor = GraphSupervisor()


def supervisor_node(
    state: GraphState,
) -> GraphState:
    """
    LangGraph node.
    """

    return supervisor.create_plan(state)


def supervisor_router(
    state: GraphState,
) -> str:
    """
    Conditional edge router.
    """
    logger.info("Router state: %s", state)
    res = supervisor.route(state)
    logger.info("Router returned: %s", res)
    return res