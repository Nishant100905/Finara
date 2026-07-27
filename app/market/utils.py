"""
Market utilities.
"""

from __future__ import annotations


def percentage_change(
    current: float,
    previous: float,
) -> float:

    if previous == 0:
        return 0.0

    return ((current - previous) / previous) * 100