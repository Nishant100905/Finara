"""
Request Models
"""

from typing import Optional

from pydantic import BaseModel, Field


# ==========================================================
# Authentication
# ==========================================================

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ==========================================================
# Chat
# ==========================================================

class ChatRequest(BaseModel):

    query: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User query"
    )

    session_id: Optional[str] = None

    use_hyde: bool = True

    use_web_search: bool = True

    temperature: float = Field(
        default=0.2,
        ge=0,
        le=1,
    )

    top_k: int = Field(
        default=10,
        ge=1,
        le=20,
    )


# ==========================================================
# Health
# ==========================================================

class HealthRequest(BaseModel):

    ping: str = "ping"