"""
User Profile Repository.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models import UserProfile

from .base import BaseRepository


class ProfileRepository(
    BaseRepository[UserProfile],
):

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

    def get_by_user_id(
        self,
        user_id: str,
    ) -> UserProfile | None:

        return (
            self.db.query(UserProfile)
            .filter(
                UserProfile.user_id == user_id
            )
            .first()
        )

    def exists(
        self,
        user_id: str,
    ) -> bool:

        return (
            self.get_by_user_id(user_id)
            is not None
        )

    def save(
        self,
        profile: UserProfile,
    ) -> UserProfile:

        existing = self.get_by_user_id(
            profile.user_id
        )

        if existing:

            existing.income = profile.income
            existing.expenses = profile.expenses
            existing.savings = profile.savings
            existing.monthly_investment = (
                profile.monthly_investment
            )
            existing.investment_goal = (
                profile.investment_goal
            )
            existing.risk_tolerance = (
                profile.risk_tolerance
            )
            existing.time_horizon = (
                profile.time_horizon
            )
            existing.preferred_assets = (
                profile.preferred_assets
            )
            existing.currency = (
                profile.currency
            )

            self.commit()
            self.refresh(existing)

            return existing

        return self.add(profile)

    def remove(
        self,
        user_id: str,
    ) -> bool:

        profile = self.get_by_user_id(
            user_id
        )

        if profile is None:
            return False

        self.delete(profile)

        return True


profile_repository = ProfileRepository