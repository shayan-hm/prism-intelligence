"""Data models for the Brain Access Layer."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class BrainDocument:
    """Represents a markdown document in the brain."""
    path: Path
    title: str
    content: str
    last_modified: datetime

    @property
    def relative_path(self) -> str:
        """Return the path relative to brain root."""
        return str(self.path)


@dataclass(frozen=True)
class SearchResult:
    """Represents a search match within a document."""
    document_path: Path
    line_number: int
    line_content: str
    match_context: str

    @property
    def relative_path(self) -> str:
        """Return the path relative to brain root."""
        return str(self.document_path)