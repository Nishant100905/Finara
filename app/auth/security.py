"""
Authentication & Security Dependencies
"""

import logging

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import AuthApiError

from app.auth.supabase import supabase

logger = logging.getLogger(__name__)

security_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(
        security_scheme
    ),
):
    """
    Verify the Supabase access token and return the current user.
    """

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    token = credentials.credentials

    try:
        claims = supabase.auth.get_claims(jwt=token)

        if claims is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token.",
            )

        # Handle both old and new Supabase SDK formats
        if isinstance(claims, dict):
            payload = claims.get("claims", claims)
        else:
            payload = claims.claims

        return {
            "id": payload.get("sub"),
            "email": payload.get("email"),
            "role": payload.get("role", "authenticated"),
            "claims": payload,
        }

    except AuthApiError as e:
        logger.warning("JWT verification failed: %s", str(e))

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
        )
    except AuthApiError as e:
        logger.warning("JWT verification failed: %s", str(e))

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
        )


async def require_authenticated(
    current_user=Depends(get_current_user),
):
    """
    Require any authenticated user.
    """

    return current_user


async def require_admin(
    current_user=Depends(get_current_user),
):
    """
    Require an admin user.
    """

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required.",
        )

    return current_user