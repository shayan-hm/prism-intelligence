"""Custom exceptions for the Brain Access Layer."""


class BrainError(Exception):
    """Base exception for all Brain Access Layer errors."""
    pass


class BrainNotFoundError(BrainError):
    """Raised when a requested brain resource is not found."""
    pass


class BrainSecurityError(BrainError):
    """Raised when a security violation is detected (e.g., path traversal)."""
    pass