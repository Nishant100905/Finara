"""
Financial Profile Service.
"""

from __future__ import annotations

from .models import UserFinancialProfile


class FinancialProfileService:

    def create(
        self,
        **kwargs,
    ) -> UserFinancialProfile:

        return UserFinancialProfile(**kwargs)

    def update(
        self,
        profile: UserFinancialProfile,
        **kwargs,
    ) -> UserFinancialProfile:

        return profile.model_copy(
            update=kwargs
        )


profile_service = FinancialProfileService()