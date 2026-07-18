"""Search service for the Brain Access Layer."""

import re
from pathlib import Path
from dataclasses import dataclass

from tools.brain.config import BRAIN_ROOT
from tools.brain.exceptions import BrainSecurityError
from tools.brain.models import SearchResult


def search(query: str) -> list[SearchResult]:
    """Search for a query string across all markdown files in brain/.

    Args:
        query: The search query (case-insensitive).

    Returns:
        List of SearchResult objects with matching lines.

    Raises:
        BrainSecurityError: If query contains path traversal patterns.
    """
    if ".." in query:
        raise BrainSecurityError("Path traversal pattern in search query")

    results: list[SearchResult] = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)

    for md_file in BRAIN_ROOT.rglob("*.md"):
        # Skip hidden files and directories
        if any(part.startswith(".") for part in md_file.parts):
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        for line_num, line in enumerate(content.splitlines(), start=1):
            if pattern.search(line):
                # Get context (1 line before and after)
                lines = content.splitlines()
                start = max(0, line_num - 2)
                end = min(len(lines), line_num + 1)
                context = "\n".join(lines[start:end])

                results.append(SearchResult(
                    document_path=md_file,
                    line_number=line_num,
                    line_content=line.rstrip(),
                    match_context=context
                ))

    return results