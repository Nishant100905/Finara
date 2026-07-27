"""
Common Helper Functions
"""

import hashlib
import json
import logging
import time
import uuid
from typing import Any

logger = logging.getLogger(__name__)


# ==========================================================
# Time Utilities
# ==========================================================

def current_timestamp() -> float:
    """
    Return current UNIX timestamp.
    """
    return time.time()


def execution_time(start_time: float) -> float:
    """
    Calculate execution time in seconds.
    """
    return round(
        time.time() - start_time,
        3,
    )


# ==========================================================
# UUID
# ==========================================================

def generate_uuid() -> str:
    """
    Generate a unique UUID4 string.
    """
    return str(uuid.uuid4())


# ==========================================================
# Text Utilities
# ==========================================================

def normalize_text(text: str) -> str:
    """
    Normalize whitespace.
    """
    return " ".join(
        text.strip().split()
    )


def truncate_text(
    text: str,
    max_length: int = 200,
) -> str:
    """
    Truncate long strings.
    """

    if len(text) <= max_length:
        return text

    return text[:max_length] + "..."


# ==========================================================
# Hash Utilities
# ==========================================================

def sha256_hash(text: str) -> str:
    """
    SHA256 hash.
    """

    return hashlib.sha256(
        text.encode()
    ).hexdigest()


# ==========================================================
# JSON Utilities
# ==========================================================

def to_json(data: Any) -> str:
    """
    Convert object to JSON string.
    """

    return json.dumps(
        data,
        indent=2,
        ensure_ascii=False,
    )


def from_json(data: str):
    """
    Parse JSON string.
    """

    return json.loads(data)


# ==========================================================
# Dictionary Helpers
# ==========================================================

def remove_none(dictionary: dict):

    return {
        k: v
        for k, v in dictionary.items()
        if v is not None
    }


# ==========================================================
# Chunk Helpers
# ==========================================================

def chunk_list(
    items,
    chunk_size: int,
):

    for i in range(
        0,
        len(items),
        chunk_size,
    ):

        yield items[
            i:i + chunk_size
        ]


# ==========================================================
# Retry Helper
# ==========================================================

def retry(
    function,
    retries=3,
):

    for attempt in range(
        retries,
    ):

        try:

            return function()

        except Exception as e:

            logger.warning(
                "Retry %d/%d failed: %s",
                attempt + 1,
                retries,
                e,
            )

    raise RuntimeError(
        "Maximum retries exceeded."
    )