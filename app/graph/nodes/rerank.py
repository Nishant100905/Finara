"""
Cross Encoder Reranker

Re-ranks the merged retrieval results using
``BAAI/bge-reranker-base``. The resulting ``cross_score``
(raw logit) is later normalized via sigmoid by the relevance
check.

If the cross-encoder model is not available at runtime (e.g.
in a tiny test environment) we fall back to the input order so
the pipeline never crashes.
"""

from __future__ import annotations

import logging

from app.graph.state import GraphState

logger = logging.getLogger(__name__)

# Lazy-loaded so importing this module does not require torch.
_reranker = None


def _get_reranker():
    global _reranker
    if _reranker is not None:
        return _reranker
    try:
        from sentence_transformers import CrossEncoder
        _reranker = CrossEncoder("BAAI/bge-reranker-base")
        logger.info("[rerank] Loaded bge-reranker-base")
    except Exception as exc:
        logger.warning(
            "[rerank] CrossEncoder unavailable (%s); falling back to identity rerank.",
            exc,
        )
        _reranker = "fallback"
    return _reranker


def rerank_node(state: GraphState) -> GraphState:
    """
    Rerank ``state['merged_results']`` and write
    ``state['reranked_results']`` (top 10 by cross-encoder
    score, descending).
    """

    logger.info("=" * 70)
    logger.info("[rerank] CROSS-ENCODER RERANK STARTED")
    logger.info("=" * 70)

    query = state.get("sanitized_query", state.get("query", ""))
    merged = state.get("merged_results")
    if not merged:
        dense = state.get("dense_results") or []
        sparse = state.get("sparse_results") or []
        merged = dense + sparse

    if not merged:
        logger.info("[rerank] No merged results — nothing to rerank.")
        state["reranked_results"] = []
        return state

    reranker = _get_reranker()

    if reranker == "fallback" or reranker is None:
        # Identity rerank: trust the input order.
        for i, doc in enumerate(merged, start=1):
            doc["cross_score"] = 0.0
        state["reranked_results"] = merged[:10]
        logger.info("[rerank] Fallback rerank applied (no model).")
        return state

    pairs = [(query, doc.get("document", "")) for doc in merged]
    try:
        scores = reranker.predict(pairs)
    except Exception as exc:
        logger.exception("[rerank] Rerank predict failed: %s", exc)
        for i, doc in enumerate(merged, start=1):
            doc["cross_score"] = 0.0
        state["reranked_results"] = merged[:10]
        return state

    reranked: list[dict] = []
    for doc, score in zip(merged, scores):
        item = dict(doc)
        item["cross_score"] = float(score)
        reranked.append(item)

    reranked.sort(key=lambda x: x["cross_score"], reverse=True)
    state["reranked_results"] = reranked[:10]

    logger.info(
        "[rerank] Reranked %d chunks. Top 3 cross-scores: %s",
        len(reranked),
        [round(r["cross_score"], 4) for r in reranked[:3]],
    )
    logger.info("=" * 70)
    return state
