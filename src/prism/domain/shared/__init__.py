"""Shared domain primitives."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Generic, TypeVar
from uuid import UUID, uuid4


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Entity(Generic[T]):
    """Base entity with identity."""

    id: T

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass(frozen=True, slots=True)
class ValueObject:
    """Base value object - immutable and comparable by value."""

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ValueObject):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """Base domain event."""

    event_id: UUID
    occurred_at: datetime
    aggregate_id: UUID

    def __init__(self, aggregate_id: UUID) -> None:
        object.__setattr__(self, "event_id", uuid4())
        object.__setattr__(self, "occurred_at", datetime.now(UTC))
        object.__setattr__(self, "aggregate_id", aggregate_id)


class DomainException(Exception):
    """Base domain exception."""

    def __init__(self, message: str, code: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code or self.__class__.__name__


class EntityNotFoundError(DomainException):
    """Raised when entity is not found."""

    def __init__(self, entity_type: str, entity_id: UUID | str) -> None:
        super().__init__(f"{entity_type} with id {entity_id} not found", "ENTITY_NOT_FOUND")
        self.entity_type = entity_type
        self.entity_id = entity_id


class BusinessRuleViolationError(DomainException):
    """Raised when business rule is violated."""

    def __init__(self, rule: str, message: str) -> None:
        super().__init__(message, "BUSINESS_RULE_VIOLATION")
        self.rule = rule


class ConcurrencyError(DomainException):
    """Raised on optimistic locking conflict."""

    def __init__(self, entity_type: str, entity_id: UUID | str) -> None:
        super().__init__(
            f"{entity_type} with id {entity_id} was modified concurrently",
            "CONCURRENCY_ERROR",
        )
        self.entity_type = entity_type
        self.entity_id = entity_id