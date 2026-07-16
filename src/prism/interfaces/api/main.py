"""FastAPI application entry point."""

from prism.interfaces.api.app import create_app

app = create_app()