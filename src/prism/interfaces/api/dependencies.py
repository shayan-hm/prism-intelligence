"""Shared dependency functions."""

from typing import Annotated

from fastapi import Depends

from prism.infrastructure.config import Settings, get_settings


def get_app_settings() -> Settings:
    """Get application settings."""
    return get_settings()


AppSettings = Annotated[Settings, Depends(get_app_settings)]