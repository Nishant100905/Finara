"""
Self-RAG Reflection Node
"""

import logging

from langchain_core.prompts import ChatPromptTemplate
from app.llm import create_llm
from app.graph.state import GraphState

logger = logging.getLogger(__name__)

judge = create_llm(temperature=0)

reflection_prompt = ChatPromptTemplate.from_template(
"""
You are an evaluator.

Question:
{question}

Context:
{context}

Answer:
{answer}

Give ONLY a score between 0 and 1.
Examples:
0.91
0.44
0.82
"""
)


def self_rag_node(state: GraphState):

    logger.info("=" * 60)
    logger.info("Self-RAG Reflection")

    retries = state.get("retry_count", 0)
    state["retry_count"] = retries + 1

    context = (state.get("context") or "").strip()
    if not context:
        state["reflection_score"] = 1.0
        logger.info("Reflection skipped (no context). Score: 1.00")
        return state

    chain = reflection_prompt | judge

    try:
        response = chain.invoke(
            {
                "question": state.get("query", ""),
                "context": context,
                "answer": state.get("answer", ""),
            }
        )
        score = float(str(response.content).strip())
    except Exception:
        score = 1.0

    state["reflection_score"] = score

    logger.info(
        "Reflection Score : %.2f (retry_count=%d)",
        score,
        state["retry_count"],
    )

    return state
