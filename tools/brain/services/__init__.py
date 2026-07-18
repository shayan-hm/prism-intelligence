"""Services package for the Brain Access Layer."""

from .reader import read
from .search import search, SearchResult
from .context import get_context
from .manifest import discover_documents, BrainDocument
from .patch import BrainPatchService, PatchOperation

__all__ = [
    "read",
    "search",
    "SearchResult",
    "get_context",
    "discover_documents",
    "BrainDocument",
    "BrainPatchService",
    "PatchOperation",
]