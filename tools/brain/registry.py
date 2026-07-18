"""Registry for the Brain Access Layer.

Provides singleton service instances.
"""

from .services.reader import read
from .services.search import search
from .services.context import get_context
from .services.manifest import discover_documents
from .services.patch import BrainPatchService


# Service instances (singletons)
_reader_service = read
_search_service = search
_context_service = get_context
_manifest_service = discover_documents
_patch_service = BrainPatchService()


def get_reader():
    """Get the reader service instance."""
    return _reader_service


def get_search():
    """Get the search service instance."""
    return _search_service


def get_context():
    """Get the context service instance."""
    return _context_service


def get_manifest():
    """Get the manifest service instance."""
    return _manifest_service


def get_patch():
    """Get the patch service instance."""
    return _patch_service