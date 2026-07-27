"""
Supervisor agent for the Financial AI Multi-Agent System.
"""

from __future__ import annotations

import logging
from typing import Callable

from langchain_core.messages import AIMessage

from .router import (
    AgentType,
    agent_router,
)
from .state import FinancialState

logger = logging.getLogger(__name__)


class SupervisorAgent:
    """
    Coordinates all specialist agents.

    Responsibilities
    ----------------
    * Determine which agent executes next
    * Prevent execution loops
    * Merge outputs
    * Handle failures
    * Decide when execution is complete
    """

    MAX_ITERATIONS = 8

    def __init__(self) -> None:

        self._agents: dict[
            AgentType,
            Callable[[FinancialState], FinancialState],
        ] = {}

    # -----------------------------------------------------
    # Registration
    # -----------------------------------------------------

    def register(
        self,
        agent: AgentType,
        handler: Callable[
            [FinancialState],
            FinancialState,
        ],
    ) -> None:
        """
        Register an agent handler.
        """

        self._agents[agent] = handler

        logger.info(
            "Registered agent: %s",
            agent.value,
        )

    # -----------------------------------------------------
    # Public API
    # -----------------------------------------------------

    def execute(
        self,
        state: FinancialState,
    ) -> FinancialState:
        """
        Execute the multi-agent workflow.
        """

        state.setdefault(
            "execution_history",
            [],
        )

        state.setdefault(
            "confidence",
            0.0,
        )

        state.setdefault(
            "response",
            "",
        )

        iteration = 0

        while iteration < self.MAX_ITERATIONS:

            next_agent = self._determine_next_agent(
                state,
            )

            if next_agent is None:

                logger.info(
                    "Workflow finished."
                )

                break

            logger.info(
                "Executing %s",
                next_agent.value,
            )

            state = self._run_agent(
                next_agent,
                state,
            )

            state["execution_history"].append(
                next_agent.value
            )

            iteration += 1

        return self._finalize(state)

    # -----------------------------------------------------
    # Routing
    # -----------------------------------------------------

    def _determine_next_agent(
        self,
        state: FinancialState,
    ) -> AgentType | None:

        history = state.get(
            "execution_history",
            [],
        )

        if not history:

            return agent_router.route(
                state.get(
                    "query",
                    "",
                )
            )

        last = history[-1]

        # Prevent executing the same agent repeatedly

        if history.count(last) >= 2:

            logger.warning(
                "Detected repeated execution of %s. "
                "Ending workflow.",
                last,
            )

            return None

        # -------------------------------------------------
        # Simple execution pipeline
        # -------------------------------------------------

        if last == AgentType.PLANNER.value:

            return AgentType.COACH

        if last == AgentType.COACH.value:

            return AgentType.PORTFOLIO

        if last == AgentType.PORTFOLIO.value:

            return AgentType.MARKET

        if last == AgentType.MARKET.value:

            return AgentType.RESEARCH

        if last == AgentType.RESEARCH.value:

            return AgentType.REPORT

        if last == AgentType.REPORT.value:

            return None

        return None

    # -----------------------------------------------------
    # Agent execution
    # -----------------------------------------------------

    def _run_agent(
        self,
        agent: AgentType,
        state: FinancialState,
    ) -> FinancialState:
        """
        Execute one registered agent.
        """

        handler = self._agents.get(
            agent,
        )

        if handler is None:

            logger.warning(
                "No handler registered for %s",
                agent.value,
            )

            return state

        try:

            result = handler(state)

            if result is not None:

                state.update(result)

        except Exception:

            logger.exception(
                "Agent %s failed.",
                agent.value,
            )

            errors = state.setdefault(
                "metadata",
                {},
            )

            error_list = errors.setdefault(
                "errors",
                [],
            )

            error_list.append(
                f"{agent.value} failed."
            )

        return state

    # -----------------------------------------------------
    # Merge results
    # -----------------------------------------------------

    def _merge_outputs(
        self,
        state: FinancialState,
    ) -> str:

        pieces: list[str] = []

        if state.get("planner"):

            pieces.append(
                "Financial planning completed."
            )

        if state.get("coach"):

            pieces.append(
                "Coaching advice generated."
            )

        if state.get("portfolio"):

            pieces.append(
                "Portfolio analyzed."
            )

        if state.get("market"):

            pieces.append(
                "Market analysis completed."
            )

        if state.get("report"):

            pieces.append(
                "Financial report prepared."
            )

        return "\n".join(
            pieces,
        )
    # -----------------------------------------------------
    # Confidence calculation
    # -----------------------------------------------------

    def _calculate_confidence(
        self,
        state: FinancialState,
    ) -> float:
        """
        Estimate confidence based on completed agent outputs.
        """

        score = 0.0

        if state.get("planner"):
            score += 15

        if state.get("coach"):
            score += 15

        if state.get("portfolio"):
            score += 15

        if state.get("market"):
            score += 15

        if state.get("forecast"):
            score += 15

        if state.get("recommendations"):
            score += 10

        if state.get("report"):
            score += 15

        return min(score, 100.0)

    # -----------------------------------------------------
    # Finalization
    # -----------------------------------------------------

    def _finalize(
        self,
        state: FinancialState,
    ) -> FinancialState:
        """
        Finalize the workflow before returning the state.
        """

        state["confidence"] = self._calculate_confidence(
            state,
        )

        if not state.get("response"):

            state["response"] = self._merge_outputs(
                state,
            )

        state.setdefault(
            "messages",
            [],
        )

        state["messages"].append(
            AIMessage(
                content=state["response"],
            )
        )

        logger.info(
            "Workflow completed with confidence %.2f%%",
            state["confidence"],
        )

        return state

    # -----------------------------------------------------
    # Utilities
    # -----------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Remove all registered agents.
        """

        self._agents.clear()

        logger.info(
            "Supervisor registry cleared."
        )

    @property
    def registered_agents(
        self,
    ) -> list[str]:
        """
        Return registered agent names.
        """

        return sorted(

            agent.value

            for agent in self._agents.keys()

        )

    def has_agent(
        self,
        agent: AgentType,
    ) -> bool:
        """
        Check whether an agent is registered.
        """

        return agent in self._agents

    # -----------------------------------------------------
    # Registration Helpers
    # -----------------------------------------------------

    def register_many(
        self,
        handlers: dict[
            AgentType,
            Callable[
                [FinancialState],
                FinancialState,
            ],
        ],
    ) -> None:
        """
        Register multiple agent handlers.
        """

        for agent, handler in handlers.items():

            self.register(
                agent,
                handler,
            )


# ---------------------------------------------------------
# Singleton Supervisor
# ---------------------------------------------------------

supervisor = SupervisorAgent()


# ---------------------------------------------------------
# LangGraph Node
# ---------------------------------------------------------

def supervisor_node(
    state: FinancialState,
) -> FinancialState:
    """
    LangGraph node entry point.

    This node coordinates the execution of all
    specialist agents and returns the updated
    workflow state.
    """

    logger.info(
        "Supervisor node started."
    )

    return supervisor.execute(
        state,
    )


# ---------------------------------------------------------
# Agent Registration Utility
# ---------------------------------------------------------

def register_default_agents(
    planner_handler: Callable[
        [FinancialState],
        FinancialState,
    ] | None = None,
    coach_handler: Callable[
        [FinancialState],
        FinancialState,
    ] | None = None,
    portfolio_handler: Callable[
        [FinancialState],
        FinancialState,
    ] | None = None,
    market_handler: Callable[
        [FinancialState],
        FinancialState,
    ] | None = None,
    research_handler: Callable[
        [FinancialState],
        FinancialState,
    ] | None = None,
    report_handler: Callable[
        [FinancialState],
        FinancialState,
    ] | None = None,
) -> SupervisorAgent:
    """
    Register the standard Financial AI agents.

    Each handler is optional, allowing gradual
    integration during development.
    """

    if planner_handler:

        supervisor.register(
            AgentType.PLANNER,
            planner_handler,
        )

    if coach_handler:

        supervisor.register(
            AgentType.COACH,
            coach_handler,
        )

    if portfolio_handler:

        supervisor.register(
            AgentType.PORTFOLIO,
            portfolio_handler,
        )

    if market_handler:

        supervisor.register(
            AgentType.MARKET,
            market_handler,
        )

    if research_handler:

        supervisor.register(
            AgentType.RESEARCH,
            research_handler,
        )

    if report_handler:

        supervisor.register(
            AgentType.REPORT,
            report_handler,
        )

    logger.info(
        "Default agents registered."
    )

    return supervisor


__all__ = [
    "SupervisorAgent",
    "supervisor",
    "supervisor_node",
    "register_default_agents",
]