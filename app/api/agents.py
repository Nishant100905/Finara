"""
Multi-Agent API Router.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.agents.service import multi_agent_service
from app.api.dependencies import protected_route

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/agents",
    tags=["Multi Agent"],
)


# =====================================================
# Models
# =====================================================

class AgentRequest(BaseModel):

    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )


class AgentResponse(BaseModel):

    success: bool

    response: str

    confidence: float

    execution_history: list[str]

    metadata: dict


# =====================================================
# Endpoint
# =====================================================

@router.post(
    "/chat",
    response_model=AgentResponse,
    summary="Financial Multi-Agent Chat",
)
async def agent_chat(

    request: AgentRequest,

    user=Depends(protected_route),

):

    try:

        result = await multi_agent_service.ainvoke(

            user_id=user["id"],

            query=request.message,

        )

        return AgentResponse(

            success=True,

            response=result.get(
                "response",
                "",
            ),

            confidence=result.get(
                "confidence",
                0.0,
            ),

            execution_history=result.get(
                "execution_history",
                [],
            ),

            metadata=result.get(
                "metadata",
                {},
            ),

        )

    except Exception as exc:

        logger.exception(
            "Multi-Agent execution failed."
        )

        raise HTTPException(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail=str(exc),

        )