"""
Deterministic routing for the RAG-first pipeline.

These routers implement the user's required flow:

    embed → retrieve → rerank → relevance_check
                                          │
                          ┌───────────────┴───────────────┐
                          │                               │
                  above threshold                   below threshold
                          │                               │
                  answer_from_rag (END)                tavily → web_relevance
                                                              │
                                            ┌─────────────────┴────────────────┐
                                            │                                  │
                                      useful results                    no useful results
                                            │                                  │
                                    answer_from_web (END)              answer_from_llm (END)

Every decision is based on a numeric threshold or a structural
check (e.g. "are there any Tavily results with content?"). No
LLM is asked to make a routing decision.
"""

from __future__ import annotations

import logging

from langgraph.graph import END

from app.graph.state import GraphState

logger = logging.getLogger(__name__)


# ==========================================================
# After relevance check
# ==========================================================

def relevance_router(state: GraphState) -> str:
    """
    Route after ``relevance_check_node``.

    Returns:
        "rag"     if local chunks are good enough to answer
        "tavily"  if we should fall back to web search
    """
    if state.get("rag_decision") == "FOUND":
        logger.info("[router] relevance_router → rag (RAG DECISION: FOUND)")
        return "rag"

    logger.info("[router] relevance_router → tavily (RAG DECISION: NOT_FOUND)")
    return "tavily"


# ==========================================================
# After RAG answer generation (fallback if context refused/insufficient)
# ==========================================================

def post_rag_router(state: GraphState) -> str:
    """
    Route after ``answer_from_rag_node``.

    Returns:
        "end"     if local PDF chunks answered the question successfully
        "tavily"  if RAG context was empty, insufficient, or LLM refused
    """
    if state.get("rag_decision") == "FOUND" and state.get("answer"):
        logger.info("[router] post_rag_router → end (RAG answer produced successfully)")
        return "end"

    logger.info("[router] post_rag_router → tavily (RAG context insufficient/refused; cascading to Tavily)")
    return "tavily"



# ==========================================================
# After web relevance check
# ==========================================================

def web_relevance_router(state: GraphState) -> str:
    """
    Route after ``web_relevance_check_node``.

    Returns:
        "web"  if Tavily returned useful results
        "llm"  if Tavily had nothing useful — answer from
                general model knowledge
    """
    if state.get("tavily_decision") == "FOUND":
        logger.info(
            "[router] web_relevance_router → web (TAVILY DECISION: FOUND)"
        )
        return "web"

    logger.info(
        "[router] web_relevance_router → llm (TAVILY DECISION: NOT_FOUND)"
    )
    return "llm"


# ==========================================================
# Top-level entry router (preserved for the new builder)
# ==========================================================

def entry_router(state: GraphState) -> str:
    """
    Decide the very first node of the pipeline.

    The current build always starts with RAG — financial actions
    are handled by a separate graph. This router is kept so the
    future addition of a financial branch does not require
    touching the rest of the pipeline.
    """
    return "embed"
