"""
Hybrid Agent

Combines Enterprise RAG context with Financial tools.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from app.graph.state import GraphState
from app.llm import llm
from app.graph.prompts import SYSTEM_PROMPT


def hybrid_agent(state: GraphState):
    """
    Hybrid RAG + Financial node.
    """

    query = state.get("query", "")
    context = state.get("context", "")

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
Question:
{query}

Retrieved Context:
{context}

Instructions:

Use the retrieved context first.

If financial reasoning is required,
combine it with your financial knowledge.

Never invent facts that are not supported by
the retrieved context.
"""
        ),
    ]

    response = llm.invoke(messages)

    state["answer"] = response.content

    return state