"""
Authentication API routes.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from supabase import AuthApiError

from app.auth.security import get_current_user
from app.auth.supabase import supabase

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Authentication"])


# ==========================================================
# Request Models
# ==========================================================

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password must contain at least 8 characters.",
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class RefreshRequest(BaseModel):
    refresh_token: str


# ==========================================================
# Register
# ==========================================================

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(data: RegisterRequest):
    """
    Register a new user using Supabase Authentication.
    """

    try:
        response = supabase.auth.sign_up(
            {
                "email": data.email,
                "password": data.password,
            }
        )

        user = response.user

        if user is None:
            logger.warning("Registration failed for %s", data.email)

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to create account.",
            )

        logger.info("New user registered: %s", data.email)

        return {
            "success": True,
            "message": "Registration successful.",
            "data": {
                "user_id": user.id,
                "email": user.email,
            },
        }

    except AuthApiError as e:

        logger.warning("Registration error: %s", str(e))

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ==========================================================
# Login
# ==========================================================

@router.post(
    "/login",
    summary="Login user",
)
async def login(data: LoginRequest):
    """
    Authenticate a user using Supabase.
    """

    try:

        response = supabase.auth.sign_in_with_password(
            {
                "email": data.email,
                "password": data.password,
            }
        )

        session = response.session
        user = response.user

        if session is None or user is None:

            logger.warning("Failed login attempt: %s", data.email)

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        logger.info("User logged in: %s", data.email)

        return {
            "success": True,
            "message": "Login successful.",
            "data": {
                "access_token": session.access_token,
                "refresh_token": session.refresh_token,
                "expires_at": session.expires_at,
                "token_type": "Bearer",
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
            },
        }

    except AuthApiError:

        logger.warning("Invalid credentials: %s", data.email)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )


# ==========================================================
# Current User
# ==========================================================

@router.get(
    "/me",
    summary="Current authenticated user",
)
async def me(
    current_user=Depends(get_current_user),
):
    """
    Return the currently authenticated user.
    """

    return {
        "success": True,
        "data": current_user,
    }


# ==========================================================
# Logout
# ==========================================================

@router.post(
    "/logout",
    summary="Logout",
)
async def logout():
    """
    Logout.

    Since Supabase uses stateless JWT authentication,
    logout is performed on the client by deleting the token.
    """

    return {
        "success": True,
        "message": "Logout successful. Remove the stored access token on the client.",
    }


# ==========================================================
# Refresh Session
# ==========================================================

@router.post(
    "/refresh",
    summary="Refresh access token",
)
async def refresh_token(data: RefreshRequest):
    """
    Refresh an expired access token.
    """

    try:

        response = supabase.auth.refresh_session(
            data.refresh_token
        )

        session = response.session

        if session is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            )

        logger.info("Session refreshed successfully")

        return {
            "success": True,
            "message": "Token refreshed successfully.",
            "data": {
                "access_token": session.access_token,
                "refresh_token": session.refresh_token,
                "expires_at": session.expires_at,
                "token_type": "Bearer",
            },
        }

    except Exception as e:
     import traceback

    traceback.print_exc()

    raise HTTPException(
        status_code=400,
        detail=str(e),
    )