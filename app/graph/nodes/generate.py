"""
Backward-compatible generate node.

The deterministic RAG-first pipeline uses three specialized
answer nodes:

  - ``answer_from_rag``  (uploaded documents)
  - ``answer_from_web``  (Tavily web search)
  - ``answer_from_llm``  (model's general knowledge)

This module preserves the ``generate_node`` symbol so any
external imports keep working. The node is now a router that
delegates to the right specialized answer based on
``state['final_routing']`` if it is set, otherwise to a
generic LLM call.
"""

from __future__ import annotations

import logging
from typing import Any

from langchain_core.prompts import ChatPromptTemplate

from app.graph.nodes.answer_from_llm import answer_from_llm_node
from app.graph.nodes.answer_from_rag import answer_from_rag_node
from app.graph.nodes.answer_from_web import answer_from_web_node
from app.graph.state import GraphState
from app.llm import create_llm

logger = logging.getLogger(__name__)

llm = create_llm(temperature=0.2)


def generate_node(state: GraphState) -> GraphState:
    """
    Backward-compatible entry point.

    If the graph has already chosen a ``final_routing`` (i.e.
    the new deterministic pipeline ran the relevance checks
    and routed to one of the three answer nodes), we delegate
    to that node. Otherwise we fall back to a generic LLM call
    so this function remains safe to call directly.
    """

    final = state.get("final_routing")

    if final == "RAG":
        return answer_from_rag_node(state)
    if final == "TAVILY":
        return answer_from_web_node(state)
    if final == "LLM":
        return answer_from_llm_node(state)

    # ----- Generic fallback (legacy behavior) -----
    logger.warning(
        "[generate] No final_routing set; using generic LLM call"
    )

    query = state.get("query", "")
    context = (state.get("context") or "").strip()

    system = (
        "You are a helpful Enterprise AI Assistant. "
        "If a context is provided, prefer it."
    )
    if context:
        user = f"Context:\n{context}\n\nQuestion:\n{query}"
    else:
        user = query

    prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("user", "{q}")]
    )
    chain = prompt | llm

    try:
        response: Any = chain.invoke({"q": user})
        answer = response.content
        if isinstance(answer, list):
            answer = "\n".join(
                p.get("text", "") if isinstance(p, dict) else str(p)
                for p in answer
            )
        state["answer"] = str(answer).strip()
    except Exception as exc:
        logger.exception("[generate] LLM call failed: %s", exc)
        state["answer"] = "I'm sorry, I couldn't generate an answer."

    state["final_routing"] = "LLM"
    return state
