"""
HyDE Node

Generate hypothetical documents to improve retrieval.
"""

import logging

from langchain_core.prompts import ChatPromptTemplate
from app.llm import create_llm
from app.graph.state import GraphState

logger = logging.getLogger(__name__)

llm = create_llm(temperature=0.3)

prompt = ChatPromptTemplate.from_template(
    """
You are an expert assistant.

Given the user's question, generate three different
hypothetical answers that could appear in relevant documents.

Question:
{question}

Return only the three hypothetical passages.
"""
)


def hyde_node(state: GraphState) -> GraphState:
    logger.info("===== ENTER HYDE =====")

    query = state.get("query", "")

    logger.info("HyDE Query: %s", query)

    chain = prompt | llm

    logger.info("Calling Ollama from HyDE...")

    response = chain.invoke(
        {
            "question": query,
        }
    )

    logger.info("Ollama responded.")

    content = response.content

    if isinstance(content, list):
        content = "\n".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )

    docs = [
        line.strip()
        for line in str(content).splitlines()
        if line.strip()
    ]

    logger.info("Generated %d hypothetical passages.", len(docs))

    state["hypothetical_documents"] = docs

    logger.info("===== EXIT HYDE =====")

    return state
