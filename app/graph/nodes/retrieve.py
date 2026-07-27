"""
Hybrid Retrieval Node

Performs:
  1. Dense retrieval (ChromaDB) — filtered by ``document_ids``
     if provided, otherwise by ``user_id``.
  2. Sparse retrieval (BM25) — post-filtered by the same
     metadata so the two streams stay consistent.

Logs every retrieved document ID, the dense distance, and a
short preview of each chunk so the operator can verify the
pipeline is wired correctly.
"""

from __future__ import annotations

import logging

from rank_bm25 import BM25Okapi

from app.database.chroma import collection
from app.graph.state import GraphState

logger = logging.getLogger(__name__)

# ==========================================================
# BM25 (loaded during startup)
# ==========================================================

documents: list[str] = []
metadata: list[dict] = []
bm25: BM25Okapi | None = None


def initialize_bm25() -> None:
    """
    (Re)build the BM25 index from the current Chroma contents.
    Called on application startup and after every document
    ingestion.
    """
    global documents, metadata, bm25

    from app.rag.bm25 import bm25 as app_bm25

    results = collection.get()
    documents = results.get("documents", []) or []
    metadata = results.get("metadatas", []) or []

    tokenized = [doc.lower().split() for doc in documents]
    if tokenized:
        bm25 = BM25Okapi(tokenized)
        app_bm25.fit(documents=documents, metadata=metadata)
    else:
        bm25 = None
        app_bm25.documents = []
        app_bm25.metadata = []
        app_bm25.bm25 = None

    logger.info("[bm25] BM25 (re)initialized with %d documents", len(documents))


# Backwards-compatible alias.
def refresh_bm25_with(user_filter: str | None = None) -> None:
    initialize_bm25()


# ==========================================================
# Filter construction
# ==========================================================

def _build_where_filter(
    user_id: str | None,
    document_ids: list[str] | None,
) -> dict | None:
    if document_ids:
        if len(document_ids) == 1:
            return {"document_id": str(document_ids[0])}
        return {"document_id": {"$in": [str(d) for d in document_ids]}}
    if user_id:
        try:
            from app.database.postgres import SessionLocal
            from app.database.models import Document
            db = SessionLocal()
            try:
                user_docs = db.query(Document.id).filter(
                    Document.user_id == str(user_id),
                    Document.status == "ready",
                ).all()
                user_doc_ids = [str(d.id) for d in user_docs]
                if user_doc_ids:
                    if len(user_doc_ids) == 1:
                        return {"document_id": user_doc_ids[0]}
                    return {"document_id": {"$in": user_doc_ids}}
            finally:
                db.close()
        except Exception as exc:
            logger.warning("[retrieve] Error looking up user document IDs: %s", exc)
        return {"user_id": str(user_id)}
    return None


def _filter_results_by_meta(
    results: list[dict],
    user_id: str | None,
    document_ids: list[str] | None,
) -> list[dict]:
    if not user_id and not document_ids:
        return results
    out: list[dict] = []

    user_doc_set = set(str(d) for d in document_ids) if document_ids else set()
    if not user_doc_set and user_id:
        try:
            from app.database.postgres import SessionLocal
            from app.database.models import Document
            db = SessionLocal()
            try:
                user_docs = db.query(Document.id).filter(
                    Document.user_id == str(user_id),
                    Document.status == "ready",
                ).all()
                user_doc_set = set(str(d.id) for d in user_docs)
            finally:
                db.close()
        except Exception:
            pass

    for r in results:
        meta = r.get("metadata") or {}
        doc_id = str(meta.get("document_id")) if meta.get("document_id") else None
        if user_doc_set:
            if doc_id and doc_id not in user_doc_set:
                continue
        elif user_id:
            chunk_user = meta.get("user_id")
            if chunk_user and str(chunk_user) != str(user_id):
                continue
        out.append(r)
    return out


# ==========================================================
# Dense retrieval
# ==========================================================

def dense_search(
    embedding,
    top_k: int = 10,
    where: dict | None = None,
    user_id: str | None = None,
    document_ids: list[str] | None = None,
) -> list[dict]:
    try:
        result = collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where=where,
        )
    except Exception as exc:
        logger.warning(
            "[retrieve] ChromaDB query with where filter failed: %s", exc
        )
        result = {}

    docs = (result.get("documents") or [[]])[0]
    metas = (result.get("metadatas") or [[]])[0]
    distances = (result.get("distances") or [[]])[0]

    dense: list[dict] = []
    for doc, meta, dist in zip(docs, metas, distances):
        dense.append(
            {
                "document": doc,
                "metadata": meta or {},
                "score": float(dist),     # raw L2 distance
                "distance": float(dist),
                "source": "dense",
            }
        )

    # Post-filter for legacy chunks that lack user_id.
    dense = _filter_results_by_meta(dense, user_id, document_ids)

    # If the filtered query returned nothing, retry without the
    # where filter and post-filter in Python. This handles
    # documents that were ingested before user_id was added.
    if not dense and where:
        try:
            fallback = collection.query(
                query_embeddings=[embedding],
                n_results=top_k * 2,
            )
            docs = (fallback.get("documents") or [[]])[0]
            metas = (fallback.get("metadatas") or [[]])[0]
            distances = (fallback.get("distances") or [[]])[0]
            dense = []
            for doc, meta, dist in zip(docs, metas, distances):
                dense.append(
                    {
                        "document": doc,
                        "metadata": meta or {},
                        "score": float(dist),
                        "distance": float(dist),
                        "source": "dense",
                    }
                )
            dense = _filter_results_by_meta(dense, user_id, document_ids)
        except Exception as exc:
            logger.warning("[retrieve] Fallback Chroma query failed: %s", exc)

    return dense[:top_k]


# ==========================================================
# Sparse retrieval
# ==========================================================

def sparse_search(
    query: str,
    top_k: int = 10,
    user_id: str | None = None,
    document_ids: list[str] | None = None,
) -> list[dict]:
    if bm25 is None:
        return []

    scores = bm25.get_scores(query.lower().split())
    ranked = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True,
    )[: max(top_k * 3, top_k)]

    sparse: list[dict] = []
    for idx, score in ranked:
        if idx >= len(documents):
            continue
        sparse.append(
            {
                "document": documents[idx],
                "metadata": metadata[idx] if idx < len(metadata) else {},
                "score": float(score),
                "source": "bm25",
            }
        )
    sparse = _filter_results_by_meta(sparse, user_id, document_ids)
    return sparse[:top_k]


# ==========================================================
# LangGraph node
# ==========================================================

def retrieve_node(state: GraphState) -> GraphState:
    """
    Hybrid retrieval node.

    Reads:
      - state['query_embedding']
      - state['sanitized_query'] / state['query']
      - state['user_id']
      - state['document_ids']

    Writes:
      - state['dense_results']
      - state['sparse_results']
    """

    logger.info("=" * 70)
    logger.info("[retrieve] HYBRID RETRIEVAL STARTED")
    logger.info("=" * 70)

    embedding = state.get("query_embedding")
    if embedding is None:
        logger.error("[retrieve] No query_embedding in state — aborting retrieve.")
        state["dense_results"] = []
        state["sparse_results"] = []
        return state

    query = state.get("sanitized_query", state.get("query", ""))
    user_id = state.get("user_id")
    document_ids = state.get("document_ids") or []

    where_filter = _build_where_filter(user_id, document_ids)
    logger.info(
        "[retrieve] filter user_id=%s document_ids=%s",
        user_id,
        document_ids,
    )

    dense_results = dense_search(
        embedding,
        top_k=10,
        where=where_filter,
        user_id=user_id,
        document_ids=document_ids,
    )
    sparse_results = sparse_search(
        query,
        top_k=10,
        user_id=user_id,
        document_ids=document_ids,
    )

    state["dense_results"] = dense_results
    state["sparse_results"] = sparse_results

    all_results = dense_results + sparse_results
    logger.info("[retrieve] Retrieved chunks (dense=%d, sparse=%d, total=%d)",
                len(dense_results), len(sparse_results), len(all_results))

    doc_ids = sorted({
        str((r.get("metadata") or {}).get("document_id", "<unknown>"))
        for r in all_results
    })
    logger.info("[retrieve] Retrieved document IDs: %s", doc_ids)

    for i, r in enumerate(all_results, start=1):
        chunk_text = (r.get("document") or "").strip()
        snippet = chunk_text[:200].replace("\n", " ")
        logger.info("  [#%d] src=%s doc=%s  preview=%s",
                    i,
                    r.get("source"),
                    (r.get("metadata") or {}).get("document_id"),
                    snippet)

    logger.info("=" * 70)
    return state
