"""
LangGraph workflow definition for the Financial Multi-Agent System.
"""

from __future__ import annotations

import logging

from langgraph.graph import END, StateGraph

from .coach_agent import coach_node
from .market_agent import market_node
from .planner_agent import planner_node
from .portfolio_agent import portfolio_node
from .report_agent import report_node
from .research_agent import research_node
from .state import FinancialState
from .supervisor import supervisor_node

logger = logging.getLogger(__name__)


class FinancialAgentGraph:
    """
    Builds and compiles the Financial Multi-Agent workflow.
    """

    def __init__(self) -> None:

        self.builder = StateGraph(
            FinancialState,
        )

        self._register_nodes()

        self._register_edges()

        self.graph = self.builder.compile()

    def _register_nodes(
        self,
    ) -> None:

        logger.info(
            "Registering LangGraph nodes."
        )

        self.builder.add_node(
            "supervisor",
            supervisor_node,
        )

        self.builder.add_node(
            "planner",
            planner_node,
        )

        self.builder.add_node(
            "coach",
            coach_node,
        )

        self.builder.add_node(
            "portfolio",
            portfolio_node,
        )

        self.builder.add_node(
            "market",
            market_node,
        )

        self.builder.add_node(
            "research",
            research_node,
        )

        self.builder.add_node(
            "report",
            report_node,
        )

    def _register_edges(
        self,
    ) -> None:

        logger.info(
            "Registering workflow edges."
        )

        self.builder.set_entry_point(
            "supervisor",
        )

        self.builder.add_edge(
            "supervisor",
            "planner",
        )

        self.builder.add_edge(
            "planner",
            "coach",
        )

        self.builder.add_edge(
            "coach",
            "portfolio",
        )

        self.builder.add_edge(
            "portfolio",
            "market",
        )

        self.builder.add_edge(
            "market",
            "research",
        )

        self.builder.add_edge(
            "research",
            "report",
        )

        self.builder.add_edge(
            "report",
            END,
        )

    def invoke(
        self,
        state: FinancialState,
    ) -> FinancialState:

        logger.info(
            "Executing Financial Agent Graph."
        )

        return self.graph.invoke(
            state,
        )

    async def ainvoke(
        self,
        state: FinancialState,
    ) -> FinancialState:

        logger.info(
            "Executing Financial Agent Graph asynchronously."
        )

        return await self.graph.ainvoke(
            state,
        )


financial_agent_graph = FinancialAgentGraph()


def get_graph():

    return financial_agent_graph.graph