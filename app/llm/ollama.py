"""
Ollama LLM
"""

from langchain_ollama import ChatOllama

from app.config.settings import settings

_llm: ChatOllama | None = None


def get_llm() -> ChatOllama:
    global _llm

    if _llm is None:

        _llm = ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.2,
            num_ctx=32768,
        )

    return _llm
