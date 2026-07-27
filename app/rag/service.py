"""
Enterprise RAG Service.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from app.rag.generator import generator
from app.rag.reranker import reranker
from app.rag.retrieval import retriever
from app.rag.spotlight import spotlight

logger = logging.getLogger(__name__)


@dataclass
class RAGResponse:
    answer: str
    context: str
    sources: list

    def model_dump(self):
        return {
            "answer": self.answer,
            "context": self.context,
            "sources": self.sources,
        }


class RAGService:

    def query(
        self,
        question: str,
        top_k: int = 5,
    ) -> RAGResponse:
        logger.info("RAGService processing query: %s", question)

        # Step 1: Hybrid retrieval (dense + sparse with RRF)
        retrieved_docs = retriever.retrieve(question, top_k=max(top_k * 2, 10))

        if not retrieved_docs:
            logger.info("No documents retrieved for query.")
            return RAGResponse(
                answer="No relevant information was found in the uploaded documents.",
                context="",
                sources=[],
            )

        # Step 2: Cross-encoder reranking
        reranked_docs = reranker.rerank(question, retrieved_docs)
        top_docs = reranked_docs[:top_k]

        # Step 3: Build context using Spotlight builder
        context = spotlight.build_context(top_docs)

        # Step 4: Generate grounded answer
        if not context.strip():
            answer = "No relevant information was found in the uploaded documents."
        else:
            try:
                answer = generator.generate(question, context)
            except Exception as exc:
                logger.exception("Generator failed during RAG query: %s", exc)
                answer = "Unable to generate an answer at this time."

        sources = [doc.get("metadata", {}) for doc in top_docs]

        return RAGResponse(
            answer=answer,
            context=context,
            sources=sources,
        )


rag_service = RAGService()