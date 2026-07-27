"""
Document Management API
Enterprise RAG System
"""

import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, protected_route
from app.database.models import Document
from app.database.chroma import collection
from app.graph.nodes.retrieve import initialize_bm25
from app.storage.supabase_storage import supabase_storage
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


# ==========================================================
# List Documents
# ==========================================================

@router.get("")
async def list_documents(
    user=Depends(protected_route),
    db: Session = Depends(get_db),
):

    documents = (
        db.query(Document)
        .filter(Document.user_id == user["id"])
        .order_by(Document.created_at.desc())
        .all()
    )

    return [
        {
            "id": doc.id,
            "filename": doc.original_filename,
            "file_type": doc.file_type,
            "file_size": doc.file_size,
            "chunk_count": doc.chunk_count,
            "page_count": doc.page_count,
            "status": doc.status,
            "uploaded_at": doc.created_at,
        }
        for doc in documents
    ]


# ==========================================================
# Document Details
# ==========================================================

@router.get("/{document_id}")
async def get_document(
    document_id: str,
    user=Depends(protected_route),
    db: Session = Depends(get_db),
):

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == user["id"],
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return {
        "id": document.id,
        "filename": document.original_filename,
        "stored_filename": document.stored_filename,
        "file_type": document.file_type,
        "file_size": document.file_size,
        "chunk_count": document.chunk_count,
        "page_count": document.page_count,
        "status": document.status,
        "created_at": document.created_at,
    }


# ==========================================================
# Delete Document
# ==========================================================

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    user=Depends(protected_route),
    db: Session = Depends(get_db),
):

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == user["id"],
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    # --------------------------------------
    # Delete vectors from Chroma
    # --------------------------------------

    results = collection.get(
        where={
            "document_id": document.id,
        }
    )

    ids = results.get("ids", [])

    if ids:
        collection.delete(ids=ids)

    # --------------------------------------
    # Delete file from Supabase Storage
    # --------------------------------------

    try:
        supabase_storage.delete_file(document.stored_filename)
        logger.info(f"Deleted file from Supabase Storage: {document.stored_filename}")
    except Exception as e:
        logger.error(f"Failed to delete file from Supabase Storage: {e}")
        # Continue with deletion even if storage cleanup fails

    # --------------------------------------
    # Delete database record
    # --------------------------------------

    db.delete(document)
    db.commit()

    # --------------------------------------
    # Refresh BM25
    # --------------------------------------

    initialize_bm25()

    return {
        "success": True,
        "message": "Document deleted successfully.",
    }