"""
Web Relevance Check

Decides whether the Tavily results are actually useful.

We treat a Tavily result set as "useful" when:
  - at least one result is present, AND
  - the result has non-empty content (we never trust a
    title-only row).

This is intentionally a hard structural check, not an LLM
judge, so the routing stays deterministic and production-ready.
"""

from __future__ import annotations

import logging

from app.graph.state import GraphState

logger = logging.getLogger(__name__)


def web_relevance_check_node(state: GraphState) -> GraphState:
    """
    Inspect ``state['web_results']`` and set
    ``state['tavily_decision']`` to "FOUND" or "NOT_FOUND".
    """

    logger.info("=" * 70)
    logger.info("[web_relevance] WEB RELEVANCE CHECK STARTED")
    logger.info("=" * 70)

    web_results = state.get("web_results") or []

    useful = [
        r for r in web_results
        if (r.get("content") or "").strip()
        or (r.get("url") or "").strip()
    ]

    if useful:
        state["tavily_decision"] = "FOUND"
    else:
        state["tavily_decision"] = "NOT_FOUND"

    metadata = state.get("metadata") or {}
    metadata["tavily_decision"] = state["tavily_decision"]
    metadata["tavily_useful_count"] = len(useful)
    state["metadata"] = metadata

    logger.info("[web_relevance] Tavily results received: %d", len(web_results))
    logger.info("[web_relevance] Useful web results       : %d", len(useful))
    logger.info("[web_relevance] TAVILY DECISION          : %s", state["tavily_decision"])
    logger.info("=" * 70)

    return state
