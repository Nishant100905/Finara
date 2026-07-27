"""
Supabase Storage Service
"""
from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import BinaryIO, Optional, Union

from supabase import Client, create_client
from supabase.lib.client_options import ClientOptions
from supabase import StorageException

from app.config.settings import settings
from app.config.logging import setup_logging

logger = setup_logging()


class SupabaseStorageService:
    """Service for interacting with Supabase Storage buckets."""

    def __init__(self):
        # Use service role key for storage operations to bypass RLS
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY
        )
        self.bucket_name = "documents"
        # Try to ensure the bucket exists (may fail if insufficient permissions)
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self) -> None:
        """Ensure the documents bucket exists."""
        try:
            # Try to get bucket info
            buckets = self.client.storage.list_buckets()
            bucket_names = [bucket.name for bucket in buckets]

            if self.bucket_name not in bucket_names:
                logger.info(f"Creating Supabase storage bucket: {self.bucket_name}")
                self.client.storage.create_bucket(
                    self.bucket_name,
                    options={"public": False}  # Private bucket for security
                )
                logger.info(f"Bucket {self.bucket_name} created successfully")
            else:
                logger.debug(f"Bucket {self.bucket_name} already exists")
        except Exception as e:
            # Log but don't fail - bucket might be created manually or via migration
            # or the service role might not have permission to create buckets
            logger.warning(f"Could not verify/create bucket {self.bucket_name}: {e}")

    def upload_file(
        self,
        file_data: Union[BinaryIO, str, bytes, os.PathLike],
        file_path: str,
        content_type: str = "application/octet-stream",
    ) -> str:
        """
        Upload a file to Supabase Storage.

        Args:
            file_data: File-like object, file path string, bytes, or path-like object containing the data
            file_path: Path within the bucket (e.g., "user_123/doc_456.pdf")
            content_type: MIME type of the file

        Returns:
            The public URL of the uploaded file
        """
        try:
            # Upload to Supabase Storage
            res = self.client.storage.from_(self.bucket_name).upload(
                file_path,
                file_data,
                {"content-type": content_type}
            )

            # Get public URL (works even for private buckets with signed URLs)
            # For private buckets, we'll need to generate signed URLs when accessing
            public_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{self.bucket_name}/{file_path}"

            logger.info(f"File uploaded to Supabase Storage: {file_path}")
            return public_url

        except StorageException as e:
            logger.error(f"Supabase Storage error uploading {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error uploading {file_path} to Supabase Storage: {e}")
            raise

    def download_file(self, file_path: str) -> bytes:
        """
        Download a file from Supabase Storage.

        Args:
            file_path: Path within the bucket

        Returns:
            File contents as bytes
        """
        try:
            res = self.client.storage.from_(self.bucket_name).download(file_path)
            logger.info(f"File downloaded from Supabase Storage: {file_path}")
            return res
        except StorageException as e:
            logger.error(f"Supabase Storage error downloading {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error downloading {file_path} from Supabase Storage: {e}")
            raise

    def delete_file(self, file_path: str) -> None:
        """
        Delete a file from Supabase Storage.

        Args:
            file_path: Path within the bucket
        """
        try:
            self.client.storage.from_(self.bucket_name).remove([file_path])
            logger.info(f"File deleted from Supabase Storage: {file_path}")
        except StorageException as e:
            logger.error(f"Supabase Storage error deleting {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error deleting {file_path} from Supabase Storage: {e}")
            raise

    def get_file_url(self, file_path: str, expires_in: int = 3600) -> str:
        """
        Get a signed URL for accessing a private file.

        Args:
            file_path: Path within the bucket
            expires_in: URL expiration time in seconds (default 1 hour)

        Returns:
            Signed URL for temporary access
        """
        try:
            res = self.client.storage.from_(self.bucket_name).create_signed_url(
                file_path, expires_in
            )
            signed_url = res.get('signedURL')
            if not signed_url:
                raise Exception("Failed to generate signed URL")
            logger.debug(f"Generated signed URL for {file_path}")
            return signed_url
        except StorageException as e:
            logger.error(f"Supabase Storage error generating signed URL for {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error generating signed URL for {file_path}: {e}")
            raise


# Singleton instance
supabase_storage = SupabaseStorageService()