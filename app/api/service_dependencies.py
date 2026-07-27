"""
Service Dependencies
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.agents.service import multi_agent_service


def get_multi_agent_service(
    db: Session = Depends(get_db),
):
    """
    Return the singleton MultiAgentService.

    The db dependency is kept so this function remains compatible
    with FastAPI dependency injection and can be extended later.
    """
    return multi_agent_service