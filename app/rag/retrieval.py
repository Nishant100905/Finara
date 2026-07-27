"""
Hybrid Retrieval
"""

import logging

from app.database.chroma import collection
from app.rag.bm25 import bm25

logger = logging.getLogger(__name__)


class HybridRetriever:

    def dense_search(
        self,
        embedding,
        top_k=10,
    ):

        response = collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

        docs = response["documents"][0]
        metas = response["metadatas"][0]
        scores = response["distances"][0]

        results = []

        for doc, meta, score in zip(
            docs,
            metas,
            scores,
        ):

            results.append(
                {
                    "document": doc,
                    "metadata": meta,
                    "score": float(score),
                }
            )

        return results

    def sparse_search(
        self,
        query,
        top_k=10,
    ):

        return bm25.search(
            query,
            top_k,
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 10,
    ):
        from app.llm.embeddings import embeddings
        from app.rag.rrf import rrf

        try:
            query_embedding = embeddings.embed_query(query)
            dense_results = self.dense_search(query_embedding, top_k=top_k)
        except Exception as exc:
            logger.warning("Dense search failed: %s", exc)
            dense_results = []

        try:
            sparse_results = self.sparse_search(query, top_k=top_k)
        except Exception as exc:
            logger.warning("Sparse search failed: %s", exc)
            sparse_results = []

        fused = rrf.fuse(dense_results, sparse_results)
        return fused[:top_k]


retriever = HybridRetriever()