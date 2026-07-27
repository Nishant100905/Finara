"""
Backward-compatible CRAG node.

The new deterministic pipeline uses ``relevance_check_node`` from
``app.graph.nodes.relevance_check``. This module is kept so any
external imports continue to work and so the log line for the
CRAG step is still produced.
"""

from __future__ import annotations

import logging

from app.graph.state import GraphState
from app.graph.nodes.relevance_check import relevance_check_node

logger = logging.getLogger(__name__)


def crag_node(state: GraphState) -> GraphState:
    """
    Thin wrapper around ``relevance_check_node`` for backward
    compatibility with older graph imports.
    """
    logger.info("[crag] Delegating to relevance_check_node")
    return relevance_check_node(state)
