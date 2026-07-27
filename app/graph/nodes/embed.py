"""
Embedding Node

Generates the query embedding used for vector search.

The Redis-backed embedding cache is intentionally bypassed on
the hot path because:

1. The cache adds an external dependency on chat latency.
2. Cached embeddings can be stale (e.g. the cache was populated
   before the user uploaded any documents, so the cached vector
   points to an empty retrieval).
3. bge-small-en-v1.5 is fast on CPU (~5-10 ms per query).

The cache module is preserved for other consumers but is not
called here.
"""

from __future__ import annotations

import logging

from app.graph.state import GraphState
from app.llm.embeddings import embeddings as shared_embeddings

logger = logging.getLogger(__name__)

embedding_model = shared_embeddings


def embed_node(state: GraphState) -> GraphState:
    """
    Embed the user query and store the vector in state.

    Sets:
      - state['query_embedding']      = list[float]
      - state['embedding_cache_hit']  = False
    """

    logger.info("=" * 70)
    logger.info("[embed] EMBEDDING NODE STARTED")
    logger.info("=" * 70)

    query = state.get(
        "sanitized_query",
        state.get("query", ""),
    )

    logger.info("[embed] CACHE BYPASSED — computing embedding directly")
    logger.info("[embed] User Question        : %s", query)

    embedding = embedding_model.embed_query(query)

    state["query_embedding"] = embedding
    state["embedding_cache_hit"] = False

    logger.info(
        "[embed] Generated Query Embedding (dim=%d, first 6 values=%s)",
        len(embedding),
        [round(x, 5) for x in embedding[:6]],
    )
    logger.info("[embed] EMBEDDING NODE COMPLETED")
    logger.info("=" * 70)

    return state
