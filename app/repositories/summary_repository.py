"""
Memory Summary Repository.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models import MemorySummary

from .base import BaseRepository


class SummaryRepository(
    BaseRepository[MemorySummary],
):

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

    def get(
        self,
        user_id: str,
    ) -> MemorySummary | None:

        return (
            self.db.query(MemorySummary)
            .filter(
                MemorySummary.user_id == user_id
            )
            .first()
        )

    def save(
        self,
        summary: MemorySummary,
    ) -> MemorySummary:

        existing = self.get(summary.user_id)

        if existing:

            existing.summary = summary.summary

            self.commit()
            self.refresh(existing)

            return existing

        return self.add(summary)

    def delete(
        self,
        user_id: str,
    ) -> bool:

        summary = self.get(user_id)

        if summary is None:
            return False

        super().delete(summary)

        return True


summary_repository = SummaryRepository