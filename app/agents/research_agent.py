"""
Research Agent.

Uses the Enterprise RAG system to answer
knowledge-based financial questions.
"""

from __future__ import annotations

import logging

from app.rag.service import rag_service

from .state import FinancialState

logger = logging.getLogger(__name__)


class ResearchAgent:
    """
    Research Agent.

    Responsibilities
    ----------------
    - Query Enterprise RAG
    - Retrieve relevant documents
    - Generate grounded answers
    - Store retrieved context
    """

    def run(
        self,
        state: FinancialState,
    ) -> FinancialState:

        logger.info(
            "Research Agent started."
        )

        query = state.get(
            "query",
            "",
        )

        metadata = state.setdefault(
            "metadata",
            {},
        )

        try:

            result = rag_service.query(
                question=query,
                top_k=5,
            )

            if hasattr(
                result,
                "model_dump",
            ):

                result_data = result.model_dump()

            elif isinstance(
                result,
                dict,
            ):

                result_data = result

            else:

                result_data = {
                    "answer": str(result),
                }

            state["rag_context"] = result_data.get(
                "context",
                "",
            )

            state["response"] = result_data.get(
                "answer",
                "",
            )

            metadata[
                "research_status"
            ] = "completed"

            metadata[
                "retrieved_documents"
            ] = len(
                result_data.get(
                    "sources",
                    [],
                )
            )

            logger.info(
                "Research Agent completed."
            )

        except Exception as exc:

            logger.exception(
                "Research Agent failed."
            )

            metadata[
                "research_status"
            ] = "failed"

            state["response"] = (
                "Unable to retrieve information."
            )

            state["rag_context"] = ""

            metadata["error"] = str(
                exc,
            )

        return state


research_agent = ResearchAgent()


def research_node(
    state: FinancialState,
) -> FinancialState:
    """
    LangGraph node.
    """

    return research_agent.run(
        state,
    )