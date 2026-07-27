"""
Answer from Uploaded Documents (RAG)

Generates a response that is **strictly grounded** in the
retrieved document chunks. The system prompt forbids the LLM
from using any external knowledge — it must answer only from
the provided <context>...</context>.

If the context is empty (which should not happen if
relevance_check_node routed us here, but we guard against it
anyway) the node returns the deterministic "no relevant
information" message instead of letting the LLM hallucinate.
"""

from __future__ import annotations

import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from app.graph.state import GraphState
from app.llm import create_llm

logger = logging.getLogger(__name__)

NO_CONTEXT_MESSAGE = (
    "No relevant information was found in the uploaded documents."
)

llm = create_llm(temperature=0.2)

RAG_SYSTEM_PROMPT = """You are an Enterprise RAG Assistant.

RULES (follow strictly):

1. Use ONLY the information inside <context>...</context> to answer
   the question. Do not use any prior or external knowledge.
2. If the <context> block is empty, or if the information required
   to answer the question is not present in the <context> block,
   respond with EXACTLY this sentence and nothing else:
   "No relevant information was found in the uploaded documents."
3. Quote or paraphrase the relevant figure/text from the context.
   State numbers, dates, and amounts explicitly.
4. Be concise and accurate. If the question cannot be answered
   from the context, do not invent an answer.
"""


REFUSAL_PHRASES = (
    "no relevant information",
    "does not contain",
    "cannot answer",
    "no relevant context",
    "not mentioned in",
    "insufficient information",
    "not provided in the context",
    "not found in the uploaded",
    "don't know based on",
    "do not know based on",
    "unable to answer",
    "context does not",
    "provided context",
)


def _is_refusal_answer(answer: str) -> bool:
    if not answer or not answer.strip():
        return True
    ans_lower = answer.lower()
    return any(phrase in ans_lower for phrase in REFUSAL_PHRASES)


def _format_prompt(query: str, context: str) -> str:
    return (
        f"{RAG_SYSTEM_PROMPT}\n\n"
        f"<context>\n{context}\n</context>\n\n"
        f"Question:\n{query}\n\nAnswer:"
    )


def _log_prompt(query: str, context: str) -> None:
    logger.info("---- Final RAG prompt sent to LLM ----")
    logger.info("%s", _format_prompt(query, context))
    logger.info("--------------------------------------")


def answer_from_rag_node(state: GraphState) -> GraphState:
    """
    Produce an answer strictly from the retrieved document context.
    If the context is empty or the LLM output is a context refusal,
    mark rag_decision = NOT_FOUND so post_rag_router cascades to Tavily.
    """

    logger.info("=" * 70)
    logger.info("[answer_rag] GENERATING ANSWER FROM UPLOADED DOCUMENTS")
    logger.info("=" * 70)

    query = state.get("query", "")
    context = (state.get("context") or "").strip()
    reranked = state.get("reranked_results") or []

    if not context and reranked:
        from app.graph.nodes.spotlight import _format_rag_context
        context = _format_rag_context(reranked)
        state["context"] = context

    if not context:
        logger.info(
            "[answer_rag] No RAG context available. Marking RAG DECISION: NOT_FOUND for Tavily fallback."
        )
        state["rag_decision"] = "NOT_FOUND"
        state["rag_used"] = False
        state["use_web_search"] = True
        state["answer"] = None
        state["tavily_invoked"] = True
        metadata = state.get("metadata") or {}
        metadata["rag_decision"] = "NOT_FOUND"
        metadata["rag_used"] = False
        metadata["use_web_search"] = True
        state["metadata"] = metadata
        return state

    _log_prompt(query, context)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", RAG_SYSTEM_PROMPT),
            (
                "user",
                "Question:\n{question}\n\nContext:\n<context>\n{context}\n</context>\n\nAnswer:",
            ),
        ]
    )
    chain = prompt | llm

    try:
        response: Any = chain.invoke(
            {"question": query, "context": context}
        )
        answer = response.content
        if isinstance(answer, list):
            answer = "\n".join(
                p.get("text", "") if isinstance(p, dict) else str(p)
                for p in answer
            )
        answer = str(answer).strip()
    except Exception as exc:
        logger.exception("[answer_rag] LLM call failed: %s", exc)
        answer = None

    if not answer or _is_refusal_answer(answer):
        logger.info(
            "[answer_rag] Document context was insufficient/refused (%s). Marking RAG DECISION: NOT_FOUND to trigger Tavily search.",
            answer,
        )
        state["rag_decision"] = "NOT_FOUND"
        state["rag_used"] = False
        state["use_web_search"] = True
        state["answer"] = None
        state["tavily_invoked"] = True

        metadata = state.get("metadata") or {}
        metadata["rag_decision"] = "NOT_FOUND"
        metadata["rag_used"] = False
        metadata["use_web_search"] = True
        state["metadata"] = metadata

        logger.info("[answer_rag] RAG DECISION UPDATED: NOT_FOUND (Cascading to Tavily)")
        logger.info("=" * 70)
        return state

    state["answer"] = answer
    state["final_routing"] = "RAG"
    state["rag_decision"] = "FOUND"
    state["sources"] = [(r.get("metadata") or {}) for r in reranked]
    state["tavily_invoked"] = False
    state["rag_used"] = True

    metadata = state.get("metadata") or {}
    metadata["final_routing"] = "RAG"
    metadata["rag_decision"] = "FOUND"
    metadata["rag_used"] = True
    state["metadata"] = metadata

    logger.info("[answer_rag] Answer length: %d characters", len(answer))
    logger.info("[answer_rag] FINAL ROUTING DECISION: RAG (Answered from Uploaded Documents)")
    logger.info("=" * 70)
    return state

