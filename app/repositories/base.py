"""
Base Repository.

Shared CRUD operations for SQLAlchemy models.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db

    def add(
        self,
        instance: ModelType,
    ) -> ModelType:

        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)

        return instance

    def delete(
        self,
        instance: ModelType,
    ) -> None:

        self.db.delete(instance)
        self.db.commit()

    def commit(
        self,
    ) -> None:

        self.db.commit()

    def refresh(
        self,
        instance: ModelType,
    ) -> None:

        self.db.refresh(instance)

    def flush(
        self,
    ) -> None:

        self.db.flush()

    def rollback(
        self,
    ) -> None:

        self.db.rollback()