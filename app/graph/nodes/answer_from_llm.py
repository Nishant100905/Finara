"""
Answer from LLM Knowledge (Final Fallback)

Runs **only** when:
  1. The RAG pipeline found no relevant document chunks, AND
  2. The Tavily web search returned no useful results.

The system prompt makes it explicit to the model that it is
answering from general knowledge, so the response itself is
honest about the source. This is the only node that lets the
LLM use its pretrained weights to answer.
"""

from __future__ import annotations

import logging
from typing import Any

from langchain_core.prompts import ChatPromptTemplate

from app.graph.state import GraphState
from app.llm import create_llm

logger = logging.getLogger(__name__)

llm = create_llm(temperature=0.4)

LLM_SYSTEM_PROMPT = """You are a helpful Enterprise AI Assistant.

Answer the user's question directly, clearly, accurately, and comprehensively using your general knowledge.
NEVER state "The context does not contain..." or "I cannot answer based on the provided context." Simply answer the question in a professional and helpful manner.
"""


def answer_from_llm_node(state: GraphState) -> GraphState:
    """
    Produce a general-knowledge answer as the final fallback.
    """

    logger.info("=" * 70)
    logger.info("[answer_llm] GENERATING ANSWER FROM LLM GENERAL KNOWLEDGE")
    logger.info("=" * 70)

    query = state.get("query", "")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", LLM_SYSTEM_PROMPT),
            ("user", "{question}"),
        ]
    )
    chain = prompt | llm

    try:
        response: Any = chain.invoke({"question": query})
        answer = response.content
        if isinstance(answer, list):
            answer = "\n".join(
                p.get("text", "") if isinstance(p, dict) else str(p)
                for p in answer
            )
        answer = str(answer).strip()
    except Exception as exc:
        logger.exception("[answer_llm] LLM call failed: %s", exc)
        answer = (
            "I'm sorry, I encountered an error while generating an "
            "answer. Please try again."
        )

    state["answer"] = answer
    state["final_routing"] = "LLM"
    state["sources"] = []
    state["tavily_invoked"] = bool(state.get("tavily_invoked") or state.get("web_results"))
    state["rag_used"] = False

    metadata = state.get("metadata") or {}
    metadata["final_routing"] = "LLM"
    state["metadata"] = metadata

    logger.info("[answer_llm] Answer length: %d characters", len(answer))
    logger.info("[answer_llm] FINAL ROUTING DECISION: LLM (Answered from General Knowledge)")
    logger.info("=" * 70)
    return state
