"""Context service for the Brain Access Layer."""

from pathlib import Path
from typing import List

from .reader import read
from tools.brain.exceptions import BrainNotFoundError, BrainSecurityError


def get_context(paths: List[str]) -> str:
    """Read multiple markdown files and concatenate them with filename headers.

    Args:
        paths: List of relative paths to markdown files from brain root.

    Returns:
        A single string containing all files with filename headers.

    Raises:
        BrainSecurityError: If any path attempts to traverse outside brain root.
        BrainNotFoundError: If any file does not exist.
    """
    if not paths:
        return ""

    parts = []
    for path in paths:
        content = read(path)
        parts.append(f"# {path}\n\n{content}")

    return "\n\n---\n\n".join(parts)