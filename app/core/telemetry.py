"""
Simple telemetry utilities.
"""

from __future__ import annotations

import time
from contextlib import contextmanager

from app.core.logging import get_logger

logger = get_logger(__name__)


@contextmanager
def track_execution(operation: str):
    """
    Measure execution time.
    """

    start = time.perf_counter()

    try:
        yield

    finally:
        elapsed = time.perf_counter() - start

        logger.info(
            "%s completed in %.3f sec",
            operation,
            elapsed,
        )


class Timer:
    """
    Manual timer.
    """

    def __init__(self):
        self.start = time.perf_counter()

    @property
    def elapsed(self):
        return time.perf_counter() - self.start