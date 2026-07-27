"""
Financial Agent Node

This node binds the LLM with all financial tools and lets the model
decide when to call a tool. The ToolNode executes the tool calls,
then control returns here until a final answer is generated.
"""

from __future__ import annotations

import logging
from typing import Any

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)

from app.graph.prompts import FINANCIAL_PROMPT
from app.graph.state import GraphState
from app.graph.tools import FINANCIAL_TOOLS
from app.llm import llm

logger = logging.getLogger(__name__)

# Bind all financial tools to the model
financial_llm = llm.bind_tools(FINANCIAL_TOOLS)


def financial_agent(state: GraphState) -> GraphState:
    """
    Financial Agent LangGraph node.

    Responsibilities:
    - Build conversation
    - Let Gemini decide whether tools are required
    - Return AIMessage (possibly containing tool calls)
    - Tool execution is handled by ToolNode
    """

    try:
        history = state.get("messages", [])

        query = state.get("query", "")

        messages: list[Any] = [
            SystemMessage(content=FINANCIAL_PROMPT)
        ]

        # Preserve conversation history
        messages.extend(history)

        # Append latest user query
        if query:
            messages.append(HumanMessage(content=query))

        response = financial_llm.invoke(messages)

        history.append(response)

        state["messages"] = history

        metadata = dict(state.get("metadata") or {})
        metadata["final_routing"] = "LLM"
        state["metadata"] = metadata

        # Save final answer only when no more tool calls exist
        if isinstance(response, AIMessage):
            if not response.tool_calls:
                state["answer"] = response.content

        logger.info("Financial agent executed successfully.")

        return state

    except Exception as exc:
        logger.exception("Financial agent failed.")

        state["error"] = str(exc)

        state["answer"] = (
            "Sorry, I encountered an error while processing "
            "your financial request."
        )

        return state


def should_continue(state: GraphState) -> str:
    """
    Router for LangGraph.

    Returns:
        "tools" -> execute ToolNode
        "end"   -> finish execution
    """

    messages = state.get("messages", [])

    if not messages:
        return "end"

    last_message = messages[-1]

    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"

    return "end"