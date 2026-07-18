"""Manifest service for the Brain Access Layer."""

from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

from tools.brain.config import BRAIN_ROOT


@dataclass(frozen=True)
class BrainDocument:
    """Metadata for a brain document."""
    path: Path
    title: str
    last_modified: datetime

    @property
    def relative_path(self) -> str:
        """Return the path relative to brain root."""
        return str(self.path.relative_to(BRAIN_ROOT))


def discover_documents() -> list[BrainDocument]:
    """Discover all markdown documents in the brain directory.

    Returns:
        List of BrainDocument objects with metadata.
    """
    documents = []

    for md_file in BRAIN_ROOT.rglob("*.md"):
        # Skip hidden files/directories
        if any(part.startswith(".") for part in md_file.parts):
            continue

        try:
            stat = md_file.stat()
            title = _extract_title(md_file)
            documents.append(BrainDocument(
                path=md_file,
                title=title,
                last_modified=datetime.fromtimestamp(stat.st_mtime)
            ))
        except (OSError, UnicodeDecodeError):
            continue

    # Sort by relative path for consistent ordering
    documents.sort(key=lambda d: d.relative_path)
    return documents


def _extract_title(md_file: Path) -> str:
    """Extract the first H1 heading as title, or use filename."""
    try:
        content = md_file.read_text(encoding="utf-8")
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
    except (OSError, UnicodeDecodeError):
        pass
    return md_file.stem