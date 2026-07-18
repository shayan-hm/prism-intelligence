"""Tests for MCP handlers."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, AsyncMock

from tools.brain.mcp.handlers import (
    handle_read_brain,
    handle_search_brain,
    handle_list_documents,
    handle_get_context,
    handle_create_document,
    handle_update_document,
    handle_append_document,
    handle_delete_document,
    handle_move_document,
    handle_apply_patch,
    handle_git_status,
    handle_git_diff,
    handle_git_log,
    handle_git_commit,
    TOOL_HANDLERS,
)


class TestReadBrain:
    """Tests for read_brain handler."""

    @pytest.mark.asyncio
    async def test_read_existing_file(self):
        """Test reading an existing file."""
        result = await handle_read_brain({"path": "README.md"})
        assert not result.isError
        assert "Prism" in result.content[0].text

    @pytest.mark.asyncio
    async def test_read_nonexistent_file(self):
        """Test reading a non-existent file."""
        result = await handle_read_brain({"path": "nonexistent.md"})
        assert result.isError
        assert "not found" in result.content[0].text.lower()

    @pytest.mark.asyncio
    async def test_read_path_traversal(self):
        """Test that path traversal is blocked."""
        result = await handle_read_brain({"path": "../../etc/passwd"})
        assert result.isError
        assert "traversal" in result.content[0].text.lower() or "security" in result.content[0].text.lower()


class TestSearchBrain:
    """Tests for search_brain handler."""

    @pytest.mark.asyncio
    async def test_search_existing_term(self):
        """Test searching for an existing term."""
        result = await handle_search_brain({"query": "Purpose"})
        assert not result.isError
        assert "match" in result.content[0].text.lower()

    @pytest.mark.asyncio
    async def test_search_nonexistent_term(self):
        """Test searching for a non-existent term."""
        result = await handle_search_brain({"query": "xyzzy_nonexistent_123"})
        assert not result.isError
        assert "no results found" in result.content[0].text.lower()


class TestListDocuments:
    """Tests for list_documents handler."""

    @pytest.mark.asyncio
    async def test_list_documents(self):
        """Test listing all documents."""
        result = await handle_list_documents({})
        assert not result.isError
        assert "Brain Document Manifest" in result.content[0].text
        assert "README.md" in result.content[0].text


class TestGetContext:
    """Tests for get_context handler."""

    @pytest.mark.asyncio
    async def test_get_context_multiple_files(self):
        """Test getting context from multiple files."""
        result = await handle_get_context({"paths": ["README.md", "knowledge/domains/market.md"]})
        assert not result.isError
        assert "README.md" in result.content[0].text
        assert "market.md" in result.content[0].text


class TestCreateDocument:
    """Tests for create_document handler."""

    @pytest.mark.asyncio
    async def test_create_document(self, tmp_path):
        """Test creating a new document."""
        from tools.brain.config import BRAIN_ROOT
        test_path = "knowledge/test_new_doc.md"
        full_path = BRAIN_ROOT / test_path

        try:
            result = await handle_create_document({
                "path": test_path,
                "content": "# Test Document\n\nContent here."
            })
            assert not result.isError
            assert "Created" in result.content[0].text
            assert full_path.exists()
            content = full_path.read_text()
            assert "Test Document" in content
        finally:
            if full_path.exists():
                full_path.unlink()

    @pytest.mark.asyncio
    async def test_create_document_non_md(self):
        """Test that non-.md files are rejected."""
        result = await handle_create_document({
            "path": "knowledge/test.txt",
            "content": "test"
        })
        assert result.isError
        assert ".md" in result.content[0].text.lower()


class TestUpdateDocument:
    """Tests for update_document handler."""

    @pytest.mark.asyncio
    async def test_update_document(self, tmp_path):
        """Test updating an existing document."""
        from tools.brain.config import BRAIN_ROOT
        test_path = "knowledge/test_update.md"
        full_path = BRAIN_ROOT / test_path

        # Create initial file
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text("# Original\n\nOld content")

        try:
            result = await handle_update_document({
                "path": test_path,
                "content": "# Updated\n\nNew content"
            })
            assert not result.isError
            assert "Updated" in result.content[0].text
            content = full_path.read_text()
            assert "Updated" in content
            assert "New content" in content
        finally:
            if full_path.exists():
                full_path.unlink()


class TestAppendDocument:
    """Tests for append_document handler."""

    @pytest.mark.asyncio
    async def test_append_document(self, tmp_path):
        """Test appending to a document."""
        from tools.brain.config import BRAIN_ROOT
        test_path = "knowledge/test_append.md"
        full_path = BRAIN_ROOT / test_path

        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text("# Original\n\nFirst section")

        try:
            result = await handle_append_document({
                "path": test_path,
                "content": "# Second\n\nAppended content"
            })
            assert not result.isError
            assert "Appended" in result.content[0].text
            content = full_path.read_text()
            assert "First section" in content
            assert "Appended content" in content
        finally:
            if full_path.exists():
                full_path.unlink()


class TestDeleteDocument:
    """Tests for delete_document handler."""

    @pytest.mark.asyncio
    async def test_delete_document(self, tmp_path):
        """Test deleting a document."""
        from tools.brain.config import BRAIN_ROOT
        test_path = "knowledge/test_delete.md"
        full_path = BRAIN_ROOT / test_path

        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text("# To Delete")

        result = await handle_delete_document({"path": test_path})
        assert not result.isError
        assert "Deleted" in result.content[0].text
        assert not full_path.exists()


class TestMoveDocument:
    """Tests for move_document handler."""

    @pytest.mark.asyncio
    async def test_move_document(self, tmp_path):
        """Test moving a document."""
        from tools.brain.config import BRAIN_ROOT
        src_path = "knowledge/test_move_src.md"
        dst_path = "knowledge/test_move_dst.md"
        src_full = BRAIN_ROOT / src_path
        dst_full = BRAIN_ROOT / dst_path

        src_full.parent.mkdir(parents=True, exist_ok=True)
        src_full.write_text("# Source")

        try:
            result = await handle_move_document({
                "source": src_path,
                "destination": dst_path
            })
            assert not result.isError
            assert "Moved" in result.content[0].text
            assert not src_full.exists()
            assert dst_full.exists()
        finally:
            if dst_full.exists():
                dst_full.unlink()


class TestApplyPatch:
    """Tests for apply_patch handler."""

    @pytest.mark.asyncio
    async def test_apply_patch_add(self, tmp_path):
        """Test adding a line via patch."""
        from tools.brain.config import BRAIN_ROOT
        test_path = "knowledge/test_patch.md"
        full_path = BRAIN_ROOT / test_path

        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text("Line 1\nLine 3\n")

        try:
            result = await handle_apply_patch({
                "path": test_path,
                "operations": [
                    {"operation": "add", "content": "Line 2", "target_line": 2}
                ]
            })
            assert not result.isError
            content = full_path.read_text()
            assert "Line 2" in content
            lines = content.strip().split("\n")
            assert lines[1] == "Line 2"
        finally:
            if full_path.exists():
                full_path.unlink()

    @pytest.mark.asyncio
    async def test_apply_patch_replace(self, tmp_path):
        """Test replacing a line via patch."""
        from tools.brain.config import BRAIN_ROOT
        test_path = "knowledge/test_patch2.md"
        full_path = BRAIN_ROOT / test_path

        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text("Old Line\nLine 2\n")

        try:
            result = await handle_apply_patch({
                "path": test_path,
                "operations": [
                    {"operation": "replace", "content": "New Line", "target_line": 1}
                ]
            })
            assert not result.isError
            content = full_path.read_text()
            assert "New Line" in content
            assert "Old Line" not in content
        finally:
            if full_path.exists():
                full_path.unlink()


class TestGitTools:
    """Tests for git tools."""

    @pytest.mark.asyncio
    async def test_git_status(self):
        """Test git status."""
        result = await handle_git_status({})
        assert not result.isError

    @pytest.mark.asyncio
    async def test_git_diff(self):
        """Test git diff."""
        result = await handle_git_diff({})
        assert not result.isError

    @pytest.mark.asyncio
    async def test_git_log(self):
        """Test git log."""
        result = await handle_git_log({"limit": 5})
        assert not result.isError

    @pytest.mark.asyncio
    async def test_git_commit_invalid_message(self):
        """Test that commit rejects non-brain messages."""
        result = await handle_git_commit({
            "message": "invalid message",
            "paths": ["README.md"]
        })
        assert result.isError
        assert "brain:" in result.content[0].text.lower()


class TestToolRegistry:
    """Tests for tool registry."""

    def test_all_tools_registered(self):
        """Test that all expected tools are registered."""
        expected = {
            "read_brain", "search_brain", "list_documents", "get_context",
            "create_document", "update_document", "append_document",
            "delete_document", "move_document", "apply_patch",
            "git_status", "git_diff", "git_log", "git_commit"
        }
        assert set(TOOL_HANDLERS.keys()) == expected