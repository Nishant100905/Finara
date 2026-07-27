"""
Reciprocal Rank Fusion (RRF)
"""

import logging

from app.graph.state import GraphState

logger = logging.getLogger(__name__)

RRF_K = 60


def reciprocal_rank(rank: int) -> float:
    return 1 / (RRF_K + rank)


def rrf_node(state: GraphState):

    logger.info("=" * 60)
    logger.info("Running RRF")

    dense = state["dense_results"]
    sparse = state["sparse_results"]

    scores = {}

    # ---------------- Dense ----------------

    for rank, doc in enumerate(dense, start=1):

        key = doc["document"]

        if key not in scores:
            scores[key] = doc.copy()
            scores[key]["rrf_score"] = 0

        scores[key]["rrf_score"] += reciprocal_rank(rank)

    # ---------------- Sparse ----------------

    for rank, doc in enumerate(sparse, start=1):

        key = doc["document"]

        if key not in scores:
            scores[key] = doc.copy()
            scores[key]["rrf_score"] = 0

        scores[key]["rrf_score"] += reciprocal_rank(rank)

    merged = sorted(
        scores.values(),
        key=lambda x: x["rrf_score"],
        reverse=True,
    )

    state["merged_results"] = merged

    logger.info(
        "Merged Documents: %d",
        len(merged),
    )

    return state