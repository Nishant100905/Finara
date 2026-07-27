#!/usr/bin/env python3
"""
Test script to verify upload functionality
"""
import os
import tempfile
from pathlib import Path

# Set up Django or FastAPI test environment if needed
# For now, just test the storage service directly

def test_storage_service():
    """Test the Supabase storage service."""
    print("Storage service imported successfully")
    print("Uploading to test/test_file.txt...")

    # Create a test file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
        temp_file.write(b"Hello, World! This is a test file.")
        temp_file_path = temp_file.name

    try:
        # Upload the file
        test_path = "test/test_file.txt"
        url = supabase_storage.upload_file(
            file_data=temp_file_path,
            file_path=test_path,
            content_type="text/plain"
        )
        print(f"Upload successful! URL: {url}")

        # Download the file
        print("Downloading file...")
        data = supabase_storage.download_file(test_path)
        print(f"Download successful! Data length: {len(data)} bytes")

        # Delete the file
        print("Deleting file...")
        supabase_storage.delete_file(test_path)
        print("Delete successful!")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up temp file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


if __name__ == "__main__":
    # Import here to avoid issues if storage service fails to load
    try:
        from app.storage.supabase_storage import supabase_storage
        test_storage_service()
    except Exception as e:
        print(f"Failed to import storage service: {e}")
        import traceback
        traceback.print_exc()