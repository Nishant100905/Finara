"""
Corrective RAG
"""

import logging

logger = logging.getLogger(__name__)

CRAG_THRESHOLD = 0.70


class CRAG:

    def evaluate(
        self,
        documents,
    ):

        if not documents:

            return {
                "score": 0,
                "use_web": True,
            }

        scores = [
            doc.get(
                "cross_score",
                0,
            )
            for doc in documents
        ]

        avg = sum(scores) / len(scores)

        return {
            "score": avg,
            "use_web": avg < CRAG_THRESHOLD,
        }


crag = CRAG()