"""
Routing functions for the LangGraph workflow.

This module is kept for backward compatibility with any code
that still imports ``crag_router`` or ``reflection_router``.
The new RAG-first pipeline uses
``app.graph.rag_router.{relevance_router, web_relevance_router}``
instead.
"""

from __future__ import annotations

import logging

from langgraph.graph import END

from app.graph.state import GraphState

logger = logging.getLogger(__name__)


def crag_router(state: GraphState) -> str:
    """
    Backward-compatible: in the new builder the relevance check
    routes directly to ``answer_from_rag`` or ``tavily``. This
    function is preserved for any callers that still expect it.
    """
    if state.get("rag_decision") == "FOUND":
        return "answer_from_rag"
    return "tavily"


def reflection_router(state: GraphState) -> str:
    """
    Backward-compatible: the deterministic pipeline no longer
    uses reflection-based retries. Always END.
    """
    return END
