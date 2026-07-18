"""Unit tests for the reader service."""

import pytest
from pathlib import Path

from tools.brain.services.reader import read
from tools.brain.exceptions import BrainNotFoundError, BrainSecurityError
from tools.brain.config import BRAIN_ROOT


class TestReader:
    """Tests for the read function."""

    def test_read_existing_file(self):
        """Test reading an existing markdown file."""
        content = read("README.md")
        assert "Prism Intelligence" in content
        assert "brain" in content.lower()

    def test_read_utf8_encoding(self):
        """Test that files are read with UTF-8 encoding."""
        content = read("README.md")
        assert isinstance(content, str)

    def test_read_nonexistent_file_raises_not_found(self):
        """Test that reading a non-existent file raises BrainNotFoundError."""
        with pytest.raises(BrainNotFoundError):
            read("nonexistent.md")

    def test_read_directory_raises_not_found(self):
        """Test that reading a directory raises BrainNotFoundError."""
        with pytest.raises(BrainNotFoundError):
            read("services")

    def test_read_path_traversal_raises_security(self):
        """Test that path traversal attempts raise BrainSecurityError."""
        with pytest.raises(BrainSecurityError):
            read("../README.md")

    def test_read_path_traversal_with_dots_raises_security(self):
        """Test that path traversal with multiple dots raises BrainSecurityError."""
        with pytest.raises(BrainSecurityError):
            read("../../etc/passwd")

    def test_read_absolute_path_outside_brain_raises_security(self):
        """Test that absolute paths outside brain raise BrainSecurityError."""
        with pytest.raises(BrainSecurityError):
            read(str(Path.home()))

    def test_read_nested_existing_file(self):
        """Test reading a nested markdown file."""
        content = read("knowledge/domains/market.md")
        assert "Purpose" in content
        assert "Responsibilities" in content

    def test_read_returns_string_not_bytes(self):
        """Test that read returns a string, not bytes."""
        content = read("README.md")
        assert isinstance(content, str)
        assert not isinstance(content, bytes)

    def test_read_knowledge_architecture_file(self):
        """Test reading architecture markdown file."""
        content = read("knowledge/architecture/architecture-v1.md")
        assert "Architecture" in content
        assert "Domain" in content

    def test_read_decisions_template(self):
        """Test reading ADR template."""
        content = read("knowledge/decisions/_template.md")
        assert "ADR" in content
        assert "Status" in content
        assert "Context" in content