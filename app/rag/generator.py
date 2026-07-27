"""
Answer Generator
"""

import logging

from langchain_core.prompts import ChatPromptTemplate
from app.llm import create_llm

logger = logging.getLogger(__name__)


class AnswerGenerator:

    def __init__(self):

        self.llm = create_llm(temperature=0.2)

        self.prompt = ChatPromptTemplate.from_template(
            """
You are an Enterprise RAG assistant.

Rules:
- Answer ONLY using the supplied context.
- Do not hallucinate.
- If the answer is unavailable, reply:
  "I don't know based on the provided documents."

Context:
{context}

Question:
{question}
"""
        )

        self.chain = self.prompt | self.llm

    def generate(
        self,
        question: str,
        context: str,
    ):

        logger.info("Generating response")

        response = self.chain.invoke(
            {
                "question": question,
                "context": context,
            }
        )

        return response.content


generator = AnswerGenerator()
