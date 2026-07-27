"""
Answer from Web (Tavily)

Generates a response that is **grounded in the Tavily web
results**. The system prompt instructs the LLM to cite the
source URLs the web node provided.

The ``context`` block has already been built by ``spotlight_node``
in the web format:

    <web id="N">Title: ... URL: ... Content: ...</web>
"""

from __future__ import annotations

import logging
from typing import Any

from langchain_core.prompts import ChatPromptTemplate

from app.graph.state import GraphState
from app.llm import create_llm

logger = logging.getLogger(__name__)

llm = create_llm(temperature=0.2)

WEB_SYSTEM_PROMPT = """You are an Enterprise Assistant with Web Search.

RULES (follow strictly):

1. Answer the question clearly, accurately, and comprehensively.
2. Use the web search context inside <context>...</context> to provide up-to-date details, and cite the source URLs provided in the web context format [Source: <url>].
3. If the web context is missing key details, supplement with your general knowledge so the user gets a helpful, complete answer.
4. NEVER refuse to answer, and NEVER output phrases like "The context does not contain..." or "I cannot answer based on the provided context." Always answer the user's question directly.
"""


def answer_from_web_node(state: GraphState) -> GraphState:
    """
    Produce a web-grounded answer with source URL citations.
    """

    logger.info("=" * 70)
    logger.info("[answer_web] GENERATING ANSWER FROM TAVILY WEB RESULTS")
    logger.info("=" * 70)

    query = state.get("query", "")
    context = (state.get("context") or "").strip()
    web_results = state.get("web_results") or []

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", WEB_SYSTEM_PROMPT),
            (
                "user",
                "Question:\n{question}\n\nWeb context:\n<context>\n{context}\n</context>\n\nAnswer (cite sources with [Source: <url>]):",
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
        logger.exception("[answer_web] LLM call failed: %s", exc)
        answer = (
            "I'm sorry, I encountered an error while generating an "
            "answer from the web search results. Please try again."
        )

    state["answer"] = answer
    state["final_routing"] = "TAVILY"
    state["sources"] = [r.get("url", "") for r in web_results if r.get("url")]
    state["tavily_invoked"] = True
    state["rag_used"] = False

    metadata = state.get("metadata") or {}
    metadata["final_routing"] = "TAVILY"
    metadata["tavily_invoked"] = True
    state["metadata"] = metadata

    logger.info("[answer_web] Answer length: %d characters", len(answer))
    logger.info("[answer_web] Source URLs  : %s",
                [r.get("url") for r in web_results if r.get("url")])
    logger.info("[answer_web] FINAL ROUTING DECISION: TAVILY (Answered from Web Search)")
    logger.info("=" * 70)
    return state
