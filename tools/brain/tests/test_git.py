"""Tests for GitService."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from tools.brain.git.service import GitService


class TestGitService:
    """Tests for GitService."""

    def test_init_finds_repo(self, tmp_path):
        """Test that GitService finds the repo root."""
        # Create a fake repo structure
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / ".git").mkdir()

        brain = repo / "brain"
        brain.mkdir()

        service = GitService(brain)
        assert service.repo_path == repo

    def test_init_not_in_repo_raises(self, tmp_path):
        """Test that GitService raises if not in a repo."""
        brain = tmp_path / "brain"
        brain.mkdir()

        with pytest.raises(FileNotFoundError):
            GitService(brain)

    def test_run_git(self, tmp_path):
        """Test running a git command."""
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / ".git").mkdir()

        service = GitService(repo)
        result = service._run_git(["status"])
        # Empty repo status is empty string
        assert isinstance(result, str)

    def test_get_status(self, tmp_path):
        """Test getting git status."""
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / ".git").mkdir()

        service = GitService(repo)
        status = service.get_status()
        assert isinstance(status, str)

    def test_get_diff(self, tmp_path):
        """Test getting git diff."""
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / ".git").mkdir()

        service = GitService(repo)
        diff = service.get_diff()
        assert isinstance(diff, str)

    def test_get_log(self, tmp_path):
        """Test getting git log."""
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / ".git").mkdir()

        service = GitService(repo)
        log = service.get_log(limit=5)
        assert isinstance(log, str)