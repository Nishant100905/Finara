"""
JWT Helper Functions
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt
from fastapi import HTTPException, status

from app.config.settings import settings


ALGORITHM = "HS256"


class JWTHandler:
    """
    JWT Utility Class
    """

    @staticmethod
    def create_access_token(
        data: Dict[str, Any],
        expires_minutes: int = 60,
    ) -> str:
        """
        Create JWT Access Token
        """

        payload = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=expires_minutes
        )

        payload.update(
            {
                "exp": expire,
                "aud": "authenticated",
            }
        )

        token = jwt.encode(
            payload,
            settings.SUPABASE_JWT_SECRET,
            algorithm=ALGORITHM,
        )

        return token

    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """
        Verify JWT
        """

        try:

            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=[ALGORITHM],
                audience="authenticated",
            )

            return payload

        except jwt.ExpiredSignatureError:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired.",
            )

        except jwt.InvalidTokenError:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token.",
            )

    @staticmethod
    def is_expired(token: str) -> bool:
        """
        Check whether token is expired.
        """

        try:

            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=[ALGORITHM],
                audience="authenticated",
            )

            exp = payload["exp"]

            return datetime.now(
                timezone.utc
            ).timestamp() > exp

        except Exception:
            return True

    @staticmethod
    def get_payload(token: str):

        return JWTHandler.verify_token(token)