"""
Upload API

Handles document uploads for Enterprise RAG using Supabase Storage.
"""

import os
import tempfile
import uuid
import logging
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, protected_route
from app.database.models import Document
from app.ingestion.ingest import ingest_document
from app.storage.supabase_storage import supabase_storage

logger = logging.getLogger(__name__)

router = APIRouter()

# ---------------------------------------------------------
# Allowed Extensions
# ---------------------------------------------------------

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".csv",
}

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


# ---------------------------------------------------------
# Upload Endpoint
# ---------------------------------------------------------

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    user=Depends(protected_route),
    db: Session = Depends(get_db),
):
    """
    Upload a document, save metadata,
    ingest into ChromaDB and update status.
    """

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail="Only PDF, DOCX, TXT and CSV files are allowed.",
        )

    # Generate unique filename for storage
    unique_filename = f"{uuid.uuid4().hex}{extension}"
    # Supabase storage path: user_{user_id}/{unique_filename}
    storage_path = f"user_{user['id']}/{unique_filename}"

    # Create temporary file for processing
    temp_file_path = None

    try:
        # Read file content into memory for size check and upload
        file_content = await file.read()
        file_size = len(file_content)

        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File exceeds the 20 MB limit.",
            )

        # Reset file position for potential reuse
        await file.seek(0)

        # -------------------------------------------------
        # Create database record
        # -------------------------------------------------

        document = Document(
            user_id=user["id"],
            original_filename=file.filename,
            stored_filename=storage_path,  # Store Supabase path
            file_type=extension.replace(".", ""),
            file_size=file_size,
            status="processing",
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        # -------------------------------------------------
        # Upload to Supabase Storage
        # -------------------------------------------------

        # Write bytes to temporary file for upload (Supabase storage expects file path)
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_upload_file:
            temp_upload_file.write(file_content)
            temp_upload_file_path = temp_upload_file.name

        try:
            # Upload file content to Supabase
            supabase_storage.upload_file(
                file_data=temp_upload_file_path,
                file_path=storage_path,
                content_type=file.content_type or "application/octet-stream"
            )
        finally:
            # Clean up temporary upload file
            if os.path.exists(temp_upload_file_path):
                os.unlink(temp_upload_file_path)

        logger.info(f"File uploaded to Supabase Storage: {storage_path}")

        # -------------------------------------------------
        # Download to temporary file for processing
        # -------------------------------------------------

        # Create temporary file
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
                temp_file_path = temp_file.name
                # Download from Supabase Storage
                file_bytes = supabase_storage.download_file(storage_path)
                temp_file.write(file_bytes)

            # -------------------------------------------------
            # Ingest document from temporary file
            # -------------------------------------------------

            result = ingest_document(
                file_path=temp_file_path,
                document_id=document.id,
                user_id=user["id"],
            )

            # -------------------------------------------------
            # Update metadata
            # -------------------------------------------------

            document.chunk_count = result.get("chunk_count", 0)
            document.page_count = result.get("page_count", 0)
            document.status = "ready"

            db.commit()

            return {
                "success": True,
                "document_id": document.id,
                "filename": document.original_filename,
                "stored_filename": document.stored_filename,  # This is the Supabase path
                "file_size": document.file_size,
                "status": document.status,
                "chunk_count": document.chunk_count,
                "page_count": document.page_count,
            }
        finally:
            # Clean up temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            "Document upload failed while processing %s.",
            file.filename,
        )

        db.rollback()

        # Clean up Supabase storage if document was created
        if 'document' in locals() and document.id:
            try:
                supabase_storage.delete_file(storage_path)
                logger.info(f"Cleaned up Supabase storage file: {storage_path}")
            except Exception as cleanup_error:
                logger.error(f"Failed to cleanup Supabase storage: {cleanup_error}")

        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception as cleanup_error:
                logger.error(f"Failed to cleanup temporary file: {cleanup_error}")

        raise HTTPException(
            status_code=500,
            detail="The document could not be processed. Please try again or contact support if the problem persists.",
        )
