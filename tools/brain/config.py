"""Configuration for the Brain Access Layer."""

from pathlib import Path


def get_repo_root() -> Path:
    """Return the repository root directory."""
    current = Path(__file__).resolve()
    while current != current.parent:
        # Check for .git first (more reliable marker of repo root)
        if (current / ".git").exists():
            return current
        # Check for pyproject.toml that contains the main project config
        pyproject = current / "pyproject.toml"
        if pyproject.exists():
            # Verify this is the root pyproject.toml by checking for brain/ dir
            if (current / "brain").exists():
                return current
        current = current.parent
    return Path.cwd()


REPO_ROOT = get_repo_root()
BRAIN_ROOT = REPO_ROOT / "brain"