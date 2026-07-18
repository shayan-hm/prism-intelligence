"""Git service for brain repository operations."""

import subprocess
from pathlib import Path
from typing import Optional


class GitService:
    """Service for git operations on the brain repository."""

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self._find_repo_root()

    def _find_repo_root(self) -> None:
        """Find the git repository root."""
        current = self.repo_path
        while current != current.parent:
            if (current / ".git").exists():
                self.repo_path = current
                return
            current = current.parent
        raise FileNotFoundError(f"Not a git repository: {self.repo_path}")

    def _run(self, args: list[str], capture: bool = True) -> subprocess.CompletedProcess:
        """Run a git command."""
        return subprocess.run(
            ["git", "-C", str(self.repo_path)] + args,
            capture_output=capture,
            text=True,
            check=False
        )

    def _run_git(self, args: list[str]) -> str:
        """Run a git command and return stdout."""
        return self._run(args).stdout.strip()

    def get_status(self) -> str:
        """Get git status."""
        result = self._run(["status", "--short"])
        return result.stdout.strip()

    def get_diff(self, path: Optional[str] = None) -> str:
        """Get git diff."""
        args = ["diff"]
        if path:
            args.append(path)
        result = self._run(args)
        return result.stdout.strip()

    def get_log(self, limit: int = 10) -> str:
        """Get git log."""
        result = self._run(["log", f"-{limit}", "--oneline", "--decorate"])
        return result.stdout.strip()

    def commit(self, message: str, paths: list[str]) -> str:
        """Stage and commit files."""
        if not message.startswith("brain:"):
            raise ValueError("Commit message must start with 'brain:'")

        # Check that all paths exist and are within repo
        for path in paths:
            full_path = (self.repo_path / path).resolve()
            try:
                full_path.relative_to(self.repo_path.resolve())
            except ValueError:
                raise ValueError(f"Path outside repository: {path}")
            if not full_path.exists():
                raise FileNotFoundError(f"File not found: {path}")

        # Stage files
        result = self._run(["add"] + paths)
        if result.returncode != 0:
            raise RuntimeError(f"git add failed: {result.stderr}")

        # Commit
        result = self._run(["commit", "-m", message])
        if result.returncode != 0:
            raise RuntimeError(f"git commit failed: {result.stderr}")

        return result.stdout.strip()