"""File reading service for the Brain Access Layer."""

from pathlib import Path

from tools.brain.config import BRAIN_ROOT
from tools.brain.exceptions import BrainNotFoundError, BrainSecurityError


def read(path: str) -> str:
    """Read a markdown file from the brain directory.

    Args:
        path: Relative path to the file within brain/ (e.g., "knowledge/domains/market.md")

    Returns:
        The file content as UTF-8 string.

    Raises:
        BrainSecurityError: If path traversal is attempted.
        BrainNotFoundError: If the file does not exist.
    """
    # Resolve the requested path
    requested = (BRAIN_ROOT / path).resolve()

    # Prevent path traversal - ensure the resolved path is within BRAIN_ROOT
    try:
        requested.relative_to(BRAIN_ROOT.resolve())
    except ValueError:
        raise BrainSecurityError(f"Path traversal attempted: {path}")

    # Check file exists and is a file (not a directory)
    if not requested.exists():
        raise BrainNotFoundError(f"File not found: {path}")

    if not requested.is_file():
        raise BrainNotFoundError(f"Path is not a file: {path}")

    # Only allow .md files
    if requested.suffix != ".md":
        raise BrainSecurityError(f"Only .md files are allowed: {path}")

    # Read with UTF-8 encoding
    return requested.read_text(encoding="utf-8")