"""
BM25 Retriever
"""

import logging

from rank_bm25 import BM25Okapi

logger = logging.getLogger(__name__)


class BM25Retriever:

    def __init__(self):

        self.documents = []
        self.metadata = []
        self.bm25 = None

    def fit(
        self,
        documents,
        metadata,
    ):

        self.documents = documents
        self.metadata = metadata

        tokenized = [
            doc.lower().split()
            for doc in documents
        ]

        self.bm25 = BM25Okapi(
            tokenized
        )

        logger.info(
            "BM25 initialized with %d documents",
            len(documents),
        )

    def search(
        self,
        query,
        top_k=10,
    ):

        if self.bm25 is None:

            return []

        scores = self.bm25.get_scores(
            query.lower().split()
        )

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True,
        )[:top_k]

        results = []

        for idx, score in ranked:

            results.append(
                {
                    "document": self.documents[idx],
                    "metadata": self.metadata[idx],
                    "score": float(score),
                }
            )

        return results


bm25 = BM25Retriever()