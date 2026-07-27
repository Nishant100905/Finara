"""
Response Models
"""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel


# ==========================================================
# Authentication
# ==========================================================

class TokenResponse(BaseModel):

    access_token: str

    refresh_token: Optional[str] = None

    token_type: str = "Bearer"


class UserResponse(BaseModel):

    id: str

    email: str

    full_name: Optional[str] = None


# ==========================================================
# Chat
# ==========================================================

class Source(BaseModel):

    document: Optional[str] = None

    metadata: Dict[str, Any] = {}


class ChatResponse(BaseModel):

    answer: str

    sources: List[Source] = []

    retrieval_score: Optional[float] = None

    reflection_score: Optional[float] = None

    cached: bool = False

    processing_time: Optional[float] = None


# ==========================================================
# Error
# ==========================================================

class ErrorResponse(BaseModel):

    success: bool = False

    error: str


# ==========================================================
# Health
# ==========================================================

class HealthResponse(BaseModel):

    status: str

    database: bool

    redis: bool

    chroma: bool