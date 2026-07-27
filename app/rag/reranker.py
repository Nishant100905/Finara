"""
Cross Encoder Reranker
"""

import logging

from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)


class CrossEncoderReranker:

    def __init__(self):

        self.model = CrossEncoder(
            "BAAI/bge-reranker-base"
        )

    def rerank(
        self,
        query,
        documents,
    ):

        if not documents:

            return []

        pairs = [
            (
                query,
                doc["document"],
            )
            for doc in documents
        ]

        scores = self.model.predict(
            pairs
        )

        results = []

        for doc, score in zip(
            documents,
            scores,
        ):

            item = doc.copy()

            item["cross_score"] = float(score)

            results.append(item)

        results.sort(
            key=lambda x: x["cross_score"],
            reverse=True,
        )

        return results


reranker = CrossEncoderReranker()