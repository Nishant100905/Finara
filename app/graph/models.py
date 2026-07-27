"""
Graph Orchestration Models

Shared models for the orchestration layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AgentType(str, Enum):
    """
    Supported execution agents.
    """

    RAG = "rag"

    FINANCIAL = "financial"

    HYBRID = "hybrid"

    MARKET = "market"

    REFLECTION = "reflection"


class ExecutionStrategy(str, Enum):
    """
    How execution should occur.
    """

    SEQUENTIAL = "sequential"

    PARALLEL = "parallel"

    CONDITIONAL = "conditional"


@dataclass(slots=True)
class ExecutionStep:
    """
    One execution step.
    """

    agent: AgentType

    description: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ExecutionPlan:
    """
    Complete execution plan.
    """

    strategy: ExecutionStrategy = ExecutionStrategy.SEQUENTIAL

    steps: list[ExecutionStep] = field(default_factory=list)

    reflection: bool = True

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def empty(self) -> bool:
        return len(self.steps) == 0

    def add(
        self,
        agent: AgentType,
        description: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Add a step to the execution plan.
        """

        self.steps.append(
            ExecutionStep(
                agent=agent,
                description=description,
                metadata=metadata or {},
            )
        )