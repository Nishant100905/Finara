"""
HyDE (Hypothetical Document Embeddings)

Generates a hypothetical answer that is later embedded to improve retrieval.
"""

import logging

from langchain_core.prompts import ChatPromptTemplate
from app.llm import create_llm

logger = logging.getLogger(__name__)

llm = create_llm(temperature=0.3)

hyde_prompt = ChatPromptTemplate.from_template(
"""
You are an expert technical writer.

Given the user's question, write a detailed document that would perfectly answer it.

Do NOT answer as an assistant.

Instead, generate a factual document that could exist inside a knowledge base.

Question:
{question}
"""
)


class HyDE:

    def __init__(self):

        self.chain = hyde_prompt | llm

    def generate(self, query: str) -> str:

        logger.info("Generating HyDE document")

        response = self.chain.invoke(
            {
                "question": query
            }
        )

        return response.content.strip()


hyde = HyDE()
