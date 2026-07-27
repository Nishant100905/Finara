"""
Chroma Vector Store
"""

from langchain_chroma import Chroma

VECTOR_DB = "vectordb"


def get_vectorstore(embeddings):

    return Chroma(
        persist_directory=VECTOR_DB,
        embedding_function=embeddings,
    )