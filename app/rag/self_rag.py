"""
Self-RAG Evaluation
"""

import logging

from langchain_core.prompts import ChatPromptTemplate
from app.llm import create_llm

logger = logging.getLogger(__name__)


class SelfRAG:

    def __init__(self):

        self.llm = create_llm(temperature=0)

        self.prompt = ChatPromptTemplate.from_template(
            """
You are an answer evaluator.

Question:
{question}

Context:
{context}

Answer:
{answer}

Evaluate the answer.

Score it from 0 to 1.

Only return a decimal number.

Example:
0.91
"""
        )

        self.chain = self.prompt | self.llm

    def evaluate(
        self,
        question,
        context,
        answer,
    ):

        logger.info("Running Self-RAG evaluation")

        response = self.chain.invoke(
            {
                "question": question,
                "context": context,
                "answer": answer,
            }
        )

        try:

            score = float(
                response.content.strip()
            )

        except Exception:

            score = 1.0

        retry = score < 0.70

        return {
            "score": score,
            "retry": retry,
        }


self_rag = SelfRAG()
