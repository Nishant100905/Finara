"""
Factory helpers for creating customized LLMs.
"""

from langchain_ollama import ChatOllama

from app.config.settings import settings


def create_llm(
    temperature: float = 0.2,
    model: str | None = None,
):
    """
    Create a configured Ollama model.
    """

    return ChatOllama(
        model=model or settings.OLLAMA_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=temperature,
        num_ctx=32768,
    )
