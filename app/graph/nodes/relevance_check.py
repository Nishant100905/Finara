"""
Relevance Check Node

Decides whether the locally-retrieved chunks are good enough to
answer the question from uploaded documents alone, or whether
we need to fall back to web search.

The decision is **deterministic** — no LLM-as-judge. The score
is a blend of:

1. The best dense cosine similarity from ChromaDB.
2. The best cross-encoder rerank score, normalized via the
   bge-reranker-base sigmoid so different model versions
   collapse to a comparable [0, 1] range.

A chunk set is considered RELEVANT if either the best dense
similarity OR the best cross-encoder sigmoid is at or above
``settings.RAG_RELEVANCE_THRESHOLD``.

The "best" score is taken from the top reranked chunk so the
final ranking step matters: a chunk that ranks #1 wins.

Logs:
  - Number of retrieved chunks
  - Top-K similarity scores (dense + cross-encoder)
  - Retrieved document IDs
  - Context preview
  - RAG decision (FOUND / NOT_FOUND)
"""

from __future__ import annotations

import logging
import math

from app.config.settings import settings
from app.graph.state import GraphState

logger = logging.getLogger(__name__)


# ==========================================================
# Score normalization
# ==========================================================

def _sigmoid(x: float) -> float:
    """Numerically-stable sigmoid."""
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    exp_x = math.exp(x)
    return exp_x / (1.0 + exp_x)


def _cosine_from_distance(distance: float) -> float:
    """
    ChromaDB returns L2 distance by default. For normalized
    embeddings (bge-small-en-v1.5 is configured with
    normalize_embeddings=True), L2 distance is bounded in
    [0, 2] and maps to cosine similarity via:

        cos_sim = 1 - (distance ** 2) / 2
    """
    try:
        return max(0.0, min(1.0, 1.0 - (float(distance) ** 2) / 2.0))
    except Exception:
        return 0.0


def _best_dense_score(reranked: list[dict]) -> float:
    """Pick the highest dense similarity present in reranked results."""
    if not reranked:
        return 0.0
    scores = []
    for r in reranked:
        # Chroma dense path
        if "score" in r and r.get("source") == "dense":
            scores.append(_cosine_from_distance(r["score"]))
        # Some retrieval helpers store the distance under other keys
        for key in ("distance", "l2_distance"):
            if key in r and r.get("source") == "dense":
                scores.append(_cosine_from_distance(r[key]))
    return max(scores) if scores else 0.0


def _best_cross_score(reranked: list[dict]) -> float:
    """Pick the highest cross-encoder sigmoid score in reranked results."""
    if not reranked:
        return 0.0
    scores = [
        _sigmoid(float(r["cross_score"]))
        for r in reranked
        if "cross_score" in r
    ]
    return max(scores) if scores else 0.0


# ==========================================================
# Node
# ==========================================================

def relevance_check_node(state: GraphState) -> GraphState:
    """
    Decide whether the local chunks are relevant.

    Side-effects on state:
      - best_relevance_score (float, max of dense / cross)
      - rag_decision ("FOUND" / "NOT_FOUND")
      - rag_used (bool)
      - use_web_search (bool, the inverse of rag_decision == "FOUND")
      - metadata['retrieval_score'], metadata['rag_decision'],
        metadata['retrieved_doc_ids'], metadata['similarity_scores']
    """

    logger.info("=" * 70)
    logger.info("[relevance] RAG RELEVANCE CHECK STARTED")
    logger.info("=" * 70)

    reranked = state.get("reranked_results") or []
    dense_results = state.get("dense_results") or []
    sparse_results = state.get("sparse_results") or []

    logger.info("[relevance] Retrieved chunks: %d (dense=%d, sparse=%d)",
                len(reranked), len(dense_results), len(sparse_results))

    # ---- Compute scores ----
    best_dense = _best_dense_score(reranked) if reranked else 0.0
    best_cross = _best_cross_score(reranked) if reranked else 0.0

    # Use the maximum of the two signals so we never under-score
    # a chunk that one retriever liked but the other didn't.
    best = max(best_dense, best_cross)
    state["best_relevance_score"] = best

    threshold = float(settings.RAG_RELEVANCE_THRESHOLD)
    is_relevant = bool(reranked) and best >= threshold

    if is_relevant:
        state["rag_decision"] = "FOUND"
        state["rag_used"] = True
        state["use_web_search"] = False
    else:
        state["rag_decision"] = "NOT_FOUND"
        state["rag_used"] = False
        state["use_web_search"] = True

    # ---- Build a context preview for the operator ----
    preview_chunks = []
    for r in reranked[:3]:
        text = (r.get("document") or "").strip().replace("\n", " ")
        if len(text) > 220:
            text = text[:220] + "…"
        preview_chunks.append(text)
    state["context_preview"] = "\n---\n".join(preview_chunks)

    # ---- Retrieved document IDs ----
    doc_ids = sorted({
        str((r.get("metadata") or {}).get("document_id", "<unknown>"))
        for r in (reranked or dense_results or sparse_results)
    })

    # ---- Per-chunk similarity scores for the log ----
    sim_log = []
    for i, r in enumerate(reranked[:10], start=1):
        meta = r.get("metadata") or {}
        cs = r.get("cross_score")
        d = r.get("score") if r.get("source") == "dense" else None
        sim_log.append(
            {
                "rank": i,
                "document_id": meta.get("document_id"),
                "filename": meta.get("filename"),
                "page": meta.get("page"),
                "cross_score": float(cs) if cs is not None else None,
                "cross_sigmoid": _sigmoid(float(cs)) if cs is not None else None,
                "dense_distance": float(d) if d is not None else None,
                "dense_cosine": _cosine_from_distance(d) if d is not None else None,
            }
        )

    # ---- Persist to metadata so the chat endpoint can return it ----
    metadata = state.get("metadata") or {}
    metadata["retrieval_score"] = best
    metadata["rag_decision"] = state["rag_decision"]
    metadata["retrieved_doc_ids"] = doc_ids
    metadata["similarity_scores"] = sim_log
    metadata["context_preview"] = state["context_preview"]
    metadata["use_web_search"] = state["use_web_search"]
    state["metadata"] = metadata

    sim_scores_str = []
    for e in sim_log[:5]:
        cs = f"{e['cross_sigmoid']:.4f}" if e.get("cross_sigmoid") is not None else "N/A"
        dc = f"{e['dense_cosine']:.4f}" if e.get("dense_cosine") is not None else "N/A"
        sim_scores_str.append(f"cross={cs}, dense={dc}")

    # ---- Logs ----
    logger.info("========== RAG RELEVANCE DEBUG ==========")
    logger.info("User Query: %s", state.get("query", ""))
    logger.info("Retrieved Chunks: %d (dense=%d, sparse=%d)", len(reranked), len(dense_results), len(sparse_results))
    logger.info("Similarity Scores: %s", sim_scores_str)
    logger.info("RAG Decision: %s", state["rag_decision"])
    logger.info("Invoking Tavily: %s", "YES" if state["rag_decision"] == "NOT_FOUND" else "NO")
    logger.info("=========================================")

    logger.info("[relevance] Best dense cosine similarity : %.4f", best_dense)
    logger.info("[relevance] Best cross-encoder sigmoid   : %.4f", best_cross)
    logger.info("[relevance] Best combined relevance      : %.4f (threshold=%.2f)",
                best, threshold)
    logger.info("[relevance] Retrieved document IDs       : %s", doc_ids)
    logger.info("[relevance] RAG DECISION                 : %s",
                state["rag_decision"])
    logger.info("---- Top-K Similarity Scores ----")
    for entry in sim_log:
        logger.info("  #%d  doc=%s  cross=%.4f  dense=%.4f",
                    entry["rank"],
                    entry.get("document_id"),
                    entry["cross_sigmoid"] or 0.0,
                    entry["dense_cosine"] or 0.0)
    logger.info("---- Context Preview (top 3 chunks) ----")
    for chunk in preview_chunks:
        logger.info("%s", chunk)
    logger.info("=" * 70)

    return state
