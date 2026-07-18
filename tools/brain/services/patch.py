"""Patch service interface for the Brain Access Layer."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PatchOperation:
    """Represents a single patch operation."""
    path: str
    operation: str  # "add", "replace", "remove"
    content: str
    target_line: Optional[int] = None


class BrainPatchService:
    """Service for applying patches to brain documents.

    This is an interface - implementation will be added later.
    """

    def apply(self, operations: list[PatchOperation]) -> None:
        """Apply a list of patch operations.

        Args:
            operations: List of patch operations to apply.

        Raises:
            NotImplementedError: This method is not yet implemented.
        """
        raise NotImplementedError("Patch service not yet implemented")

    def validate(self, operations: list[PatchOperation]) -> bool:
        """Validate patch operations before applying.

        Args:
            operations: List of patch operations to validate.

        Returns:
            True if all operations are valid.

        Raises:
            NotImplementedError: This method is not yet implemented.
        """
        raise NotImplementedError("Patch validation not yet implemented")