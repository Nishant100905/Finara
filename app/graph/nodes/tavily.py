"""
Tavily Search Node

Invokes the Tavily web search API when the RAG pipeline could
not find relevant document chunks.

Every Tavily invocation is logged explicitly so the operator
can confirm whether the fallback path was taken and how many
results came back.
"""

from __future__ import annotations

import logging

from tavily import TavilyClient

from app.config.settings import settings
from app.graph.state import GraphState

logger = logging.getLogger(__name__)

_client: TavilyClient | None = None


def _get_client() -> TavilyClient | None:
    global _client
    if _client is not None:
        return _client
    if not settings.TAVILY_API_KEY or settings.TAVILY_API_KEY == "your_tavily_api_key":
        return None
    _client = TavilyClient(api_key=settings.TAVILY_API_KEY)
    return _client


def tavily_node(state: GraphState) -> GraphState:
    """
    Run a web search for the user query. Sets:

      - state['tavily_invoked'] = True
      - state['web_results']    = list[dict]
    """

    logger.info("=" * 70)
    logger.info("[tavily] RUNNING TAVILY WEB SEARCH")
    logger.info("=" * 70)

    state["tavily_invoked"] = True
    query = state.get(
        "sanitized_query",
        state.get("query", ""),
    )

    logger.info("[tavily] Tavily Invoked: YES")
    logger.info("[tavily] Tavily Query  : %s", query)

    client = _get_client()
    if client is None:
        logger.warning(
            "[tavily] TAVILY_API_KEY is not configured. Web results will be empty."
        )
        state["web_results"] = []
        return state

    try:
        response = client.search(
            query=query,
            max_results=settings.MAX_WEB_RESULTS,
            search_depth="advanced",
        )

        results = []
        for item in response.get("results", []):
            results.append(
                {
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "content": item.get("content"),
                }
            )

        state["web_results"] = results

        logger.info("[tavily] Tavily Results Count: %d", len(results))
        for i, r in enumerate(results, start=1):
            logger.info(
                "  [%d] %s — %s",
                i,
                r.get("title", ""),
                r.get("url", ""),
            )

    except Exception as exc:
        logger.exception("[tavily] Tavily search failed: %s", exc)
        state["web_results"] = []

    metadata = state.get("metadata") or {}
    metadata["tavily_results_count"] = len(state.get("web_results") or [])
    metadata["tavily_invoked"] = True
    state["metadata"] = metadata

    logger.info("=" * 70)
    return state
