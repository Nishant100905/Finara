"""
Tool History Repository.
"""

from __future__ import annotations

from collections import Counter
from typing import Sequence

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database.models import ToolHistory

from .base import BaseRepository


class ToolRepository(
    BaseRepository[ToolHistory],
):

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

    def save(
        self,
        tool: ToolHistory,
    ) -> ToolHistory:

        return self.add(tool)

    def get_history(
        self,
        user_id: str,
        limit: int = 50,
    ) -> Sequence[ToolHistory]:

        return (
            self.db.query(ToolHistory)
            .filter(
                ToolHistory.user_id == user_id
            )
            .order_by(
                desc(ToolHistory.created_at)
            )
            .limit(limit)
            .all()
        )

    def get_by_tool(
        self,
        user_id: str,
        tool_name: str,
    ) -> Sequence[ToolHistory]:

        return (
            self.db.query(ToolHistory)
            .filter(
                ToolHistory.user_id == user_id,
                ToolHistory.tool_name == tool_name,
            )
            .order_by(
                desc(ToolHistory.created_at)
            )
            .all()
        )

    def get_last_used(
        self,
        user_id: str,
        tool_name: str,
    ) -> ToolHistory | None:

        return (
            self.db.query(ToolHistory)
            .filter(
                ToolHistory.user_id == user_id,
                ToolHistory.tool_name == tool_name,
            )
            .order_by(
                desc(ToolHistory.created_at)
            )
            .first()
        )

    def tool_statistics(
        self,
        user_id: str,
    ) -> dict:

        history = self.get_history(
            user_id=user_id,
            limit=1000,
        )

        counter = Counter(
            item.tool_name
            for item in history
        )

        return {
            "total_calls": len(history),
            "unique_tools": len(counter),
            "usage": dict(counter),
        }


tool_repository = ToolRepository