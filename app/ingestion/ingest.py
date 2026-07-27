"""
Enterprise RAG Document Ingestion
"""

import logging
import uuid
from pathlib import Path

from app.database.chroma import collection
from app.graph.nodes.retrieve import initialize_bm25
from app.ingestion.embedding import get_embeddings
from app.ingestion.loader import load_document
from app.ingestion.splitter import split_documents

logger = logging.getLogger(__name__)


def ingest_document(
    file_path: str,
    document_id: str,
    user_id: str | None = None,
):
    """
    Load, split, embed and store a document in ChromaDB.
    """

    # --------------------------------------------------
    # Load document
    # --------------------------------------------------

    documents = load_document(file_path)

    if not documents:
        raise Exception("No content found.")

    # --------------------------------------------------
    # Split document
    # --------------------------------------------------

    chunks = split_documents(documents)
    logger.info("Chunks created: %d", len(chunks))

    # --------------------------------------------------
    # Embedding model
    # --------------------------------------------------

    embedding_model = get_embeddings()

    ids = []
    texts = []
    embeddings = []
    metadatas = []

    page_numbers = set()

    filename = Path(file_path).name

    # --------------------------------------------------
    # Prepare chunks
    # --------------------------------------------------

    for chunk in chunks:

        text = chunk.page_content.strip()

        if not text:
            continue

        page = chunk.metadata.get("page", 0)

        page_numbers.add(page)

        embedding = embedding_model.embed_query(text)

        ids.append(str(uuid.uuid4()))

        texts.append(text)

        embeddings.append(embedding)

        meta = {
            "document_id": document_id,
            "source": chunk.metadata.get(
                "source",
                filename,
            ),
            "filename": filename,
            "page": page,
        }
        if user_id:
            meta["user_id"] = str(user_id)

        metadatas.append(meta)

    logger.info("Embeddings generated: %d", len(embeddings))

    # --------------------------------------------------
    # Store vectors
    # --------------------------------------------------

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    logger.info("Upload successful")

    # --------------------------------------------------
    # Refresh BM25
    # --------------------------------------------------

    initialize_bm25()

    # --------------------------------------------------
    # Return ingestion metadata
    # --------------------------------------------------

    return {
        "status": "success",
        "chunk_count": len(ids),
        "page_count": len(page_numbers),
        "message": "Document indexed successfully.",
    }