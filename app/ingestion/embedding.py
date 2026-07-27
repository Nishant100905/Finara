"""
Embedding Model
"""

from app.llm.embeddings import embeddings as shared_embeddings


def get_embeddings():
    return shared_embeddings