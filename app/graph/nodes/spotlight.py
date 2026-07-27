"""
Spotlighting Node (deterministic)

Builds the prompt context for the LLM. The content of ``context``
depends on the routing decision:

  - If the RAG pipeline found relevant chunks, ``context`` contains
    the reranked document chunks.
  - If we fell back to web search, ``context`` contains the
    Tavily results with their URLs.
  - If neither produced anything, ``context`` is empty and the
    answer node that runs after this one will answer from the
    model's general knowledge (with a clear caveat in the answer
    that no document or web source was used).
"""

from __future__ import annotations

import logging

from app.graph.state import GraphState

logger = logging.getLogger(__name__)


def _format_rag_context(reranked: list[dict]) -> str:
    parts = []
    for i, doc in enumerate(reranked, start=1):
        text = (doc.get("document") or "").strip()
        if not text:
            continue
        meta = doc.get("metadata") or {}
        filename = meta.get("filename", "uploaded document")
        page = meta.get("page")
        page_str = f", page {page}" if page else ""
        parts.append(
            f'<document id="{i}" source="{filename}"{page_str}>\n{text}\n</document>'
        )
    return "\n\n".join(parts).strip()


def _format_web_context(web_results: list[dict]) -> str:
    parts = []
    for i, doc in enumerate(web_results, start=1):
        title = doc.get("title", "")
        content = doc.get("content", "")
        url = doc.get("url", "")
        parts.append(
            f'<web id="{i}">\nTitle: {title}\nURL: {url}\nContent: {content}\n</web>'
        )
    return "\n\n".join(parts).strip()


def spotlight_node(state: GraphState) -> GraphState:
    """
    Build ``state['context']`` from whatever source the routing
    decided to use. The downstream ``answer_from_*`` node reads
    ``context`` plus the routing metadata to know what kind of
    answer to produce.
    """

    logger.info("=" * 70)
    logger.info("[spotlight] Building context for answer generation")
    reranked = state.get("reranked_results") or []
    web_results = state.get("web_results") or []

    if reranked:
        context = _format_rag_context(reranked)
        logger.info("[spotlight] Using RAG context (%d chunks)", len(reranked))
    elif web_results:
        context = _format_web_context(web_results)
        logger.info("[spotlight] Using Tavily web context (%d results)", len(web_results))
    else:
        context = ""
        logger.info("[spotlight] No context — answer will be generated from LLM knowledge")

    state["context"] = context

    metadata = state.get("metadata") or {}
    metadata["has_context"] = bool(context)
    metadata["context_length"] = len(context)
    state["metadata"] = metadata

    logger.info("[spotlight] context_length=%d has_context=%s",
                len(context), bool(context))
    logger.info("=" * 70)

    return state
