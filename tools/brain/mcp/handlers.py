"""MCP Tool handlers for Prism Brain."""

from pathlib import Path
from typing import Any

from tools.brain.services.reader import read
from tools.brain.services.search import search
from tools.brain.services.context import get_context
from tools.brain.services.manifest import discover_documents
from tools.brain.exceptions import BrainError, BrainNotFoundError, BrainSecurityError
from tools.brain.config import BRAIN_ROOT
from tools.brain.git.service import GitService
from mcp.types import CallToolResult, TextContent


def create_text_result(content: str) -> CallToolResult:
    """Create a successful text result."""
    return CallToolResult(content=[TextContent(type="text", text=content)], isError=False)


def create_error_result(error: str) -> CallToolResult:
    """Create an error result."""
    return CallToolResult(content=[TextContent(type="text", text=f"Error: {error}")], isError=True)


async def handle_read_brain(arguments: dict[str, Any]) -> CallToolResult:
    """Read a brain document."""
    path = arguments.get("path", "")
    if not path:
        return create_error_result("Path is required")

    try:
        content = read(path)
        return create_text_result(content)
    except BrainNotFoundError as e:
        return create_error_result(str(e))
    except BrainSecurityError as e:
        return create_error_result(str(e))


async def handle_search_brain(arguments: dict[str, Any]) -> CallToolResult:
    """Search brain documents."""
    query = arguments.get("query", "")
    if not query:
        return create_error_result("Query is required")

    try:
        results = search(query)
        if not results:
            return create_text_result(f"No results found for: {query}")

        lines = [f"Found {len(results)} matches for: {query}\n"]
        for r in results:
            lines.append(f"--- {r.relative_path}:{r.line_number} ---")
            lines.append(r.line_content)
            lines.append(f"Context: {r.match_context}")
            lines.append("")

        return create_text_result("\n".join(lines))
    except BrainSecurityError as e:
        return create_error_result(str(e))


async def handle_list_documents(arguments: dict[str, Any]) -> CallToolResult:
    """List all brain documents."""
    try:
        docs = discover_documents()
        if not docs:
            return create_text_result("No documents found")

        lines = ["Brain Document Manifest\n", "=" * 50]
        for doc in docs:
            lines.append(f"\nPath: {doc.relative_path}")
            lines.append(f"Title: {doc.title}")
            lines.append(f"Last Modified: {doc.last_modified.isoformat()}")

        return create_text_result("\n".join(lines))
    except Exception as e:
        return create_error_result(f"Failed to list documents: {e}")


async def handle_get_context(arguments: dict[str, Any]) -> CallToolResult:
    """Get combined context from multiple documents."""
    paths = arguments.get("paths", [])
    if not paths:
        return create_error_result("At least one path is required")

    try:
        context = get_context(paths)
        return create_text_result(context)
    except BrainNotFoundError as e:
        return create_error_result(str(e))
    except BrainSecurityError as e:
        return create_error_result(str(e))


async def handle_create_document(arguments: dict[str, Any]) -> CallToolResult:
    """Create a new brain document."""
    try:
        path = arguments.get("path", "")
        content = arguments.get("content", "")
        title = arguments.get("title", "")

        if not path:
            return create_error_result("Path is required")
        if not path.endswith(".md"):
            return create_error_result("Only .md files are allowed")

        target = (BRAIN_ROOT / path).resolve()

        # Security check
        try:
            target.relative_to(BRAIN_ROOT.resolve())
        except ValueError:
            return create_error_result("Path traversal not allowed")

        if target.exists():
            return create_error_result(f"File already exists: {path}")

        # Create parent directories
        target.parent.mkdir(parents=True, exist_ok=True)

        # Write content with title if provided
        full_content = content
        if title:
            full_content = f"# {title}\n\n{content}"

        # Atomic write
        tmp = target.with_suffix(".tmp")
        tmp.write_text(full_content, encoding="utf-8")
        tmp.replace(target)

        return create_text_result(f"Created: {path}")
    except Exception as e:
        return create_error_result(f"Create failed: {e}")


async def handle_update_document(arguments: dict[str, Any]) -> CallToolResult:
    """Update a brain document (full replace)."""
    try:
        path = arguments.get("path", "")
        content = arguments.get("content", "")

        if not path:
            return create_error_result("Path is required")
        if not path.endswith(".md"):
            return create_error_result("Only .md files are allowed")

        target = (BRAIN_ROOT / path).resolve()

        # Security check
        try:
            target.relative_to(BRAIN_ROOT.resolve())
        except ValueError:
            return create_error_result("Path traversal not allowed")

        if not target.exists():
            return create_error_result(f"File not found: {path}")

        # Atomic write
        tmp = target.with_suffix(".tmp")
        tmp.write_text(content, encoding="utf-8")
        tmp.replace(target)

        return create_text_result(f"Updated: {path}")
    except Exception as e:
        return create_error_result(f"Update failed: {e}")


async def handle_append_document(arguments: dict[str, Any]) -> CallToolResult:
    """Append content to a brain document."""
    try:
        path = arguments.get("path", "")
        content = arguments.get("content", "")
        separator = arguments.get("separator", "\n\n---\n\n")

        if not path:
            return create_error_result("Path is required")
        if not path.endswith(".md"):
            return create_error_result("Only .md files are allowed")

        target = (BRAIN_ROOT / path).resolve()

        # Security check
        try:
            target.relative_to(BRAIN_ROOT.resolve())
        except ValueError:
            return create_error_result("Path traversal not allowed")

        if not target.exists():
            return create_error_result(f"File not found: {path}")

        # Read existing content
        existing = target.read_text(encoding="utf-8")

        # Atomic write
        new_content = existing + separator + content
        tmp = target.with_suffix(".tmp")
        tmp.write_text(new_content, encoding="utf-8")
        tmp.replace(target)

        return create_text_result(f"Appended to: {path}")
    except Exception as e:
        return create_error_result(f"Append failed: {e}")


async def handle_delete_document(arguments: dict[str, Any]) -> CallToolResult:
    """Delete a brain document."""
    try:
        path = arguments.get("path", "")

        if not path:
            return create_error_result("Path is required")
        if not path.endswith(".md"):
            return create_error_result("Only .md files are allowed")

        target = (BRAIN_ROOT / path).resolve()

        # Security check
        try:
            target.relative_to(BRAIN_ROOT.resolve())
        except ValueError:
            return create_error_result("Path traversal not allowed")

        if not target.exists():
            return create_error_result(f"File not found: {path}")

        target.unlink()
        return create_text_result(f"Deleted: {path}")
    except Exception as e:
        return create_error_result(f"Delete failed: {e}")


async def handle_move_document(arguments: dict[str, Any]) -> CallToolResult:
    """Move/rename a brain document."""
    try:
        source = arguments.get("source", "")
        destination = arguments.get("destination", "")

        if not source or not destination:
            return create_error_result("Source and destination are required")
        if not source.endswith(".md") or not destination.endswith(".md"):
            return create_error_result("Only .md files are allowed")

        src = (BRAIN_ROOT / source).resolve()
        dst = (BRAIN_ROOT / destination).resolve()

        # Security checks
        try:
            src.relative_to(BRAIN_ROOT.resolve())
            dst.relative_to(BRAIN_ROOT.resolve())
        except ValueError:
            return create_error_result("Path traversal not allowed")

        if not src.exists():
            return create_error_result(f"Source not found: {source}")

        if dst.exists():
            return create_error_result(f"Destination already exists: {destination}")

        # Create parent directories
        dst.parent.mkdir(parents=True, exist_ok=True)

        # Move
        src.rename(dst)
        return create_text_result(f"Moved: {source} -> {destination}")
    except Exception as e:
        return create_error_result(f"Move failed: {e}")


async def handle_apply_patch(arguments: dict[str, Any]) -> CallToolResult:
    """Apply a patch to a brain document."""
    try:
        path = arguments.get("path", "")
        operations = arguments.get("operations", [])

        if not path:
            return create_error_result("Path is required")
        if not operations:
            return create_error_result("At least one operation is required")

        target = (BRAIN_ROOT / path).resolve()

        # Security check
        try:
            target.relative_to(BRAIN_ROOT.resolve())
        except ValueError:
            return create_error_result("Path traversal not allowed")

        if not target.exists():
            return create_error_result(f"File not found: {path}")

        content = target.read_text(encoding="utf-8")
        lines = content.splitlines(keepends=True)

        # Apply operations in reverse order to maintain line numbers
        for op in sorted(operations, key=lambda x: x.get("target_line", 0), reverse=True):
            operation = op.get("operation")
            op_content = op.get("content", "")
            target_line = op.get("target_line", 0)

            if operation == "add":
                if target_line <= 0 or target_line > len(lines) + 1:
                    return create_error_result(f"Invalid line number: {target_line}")
                lines.insert(target_line - 1, op_content + ("\n" if not op_content.endswith("\n") else ""))
            elif operation == "replace":
                if target_line <= 0 or target_line > len(lines):
                    return create_error_result(f"Invalid line number: {target_line}")
                lines[target_line - 1] = op_content + ("\n" if not op_content.endswith("\n") else "")
            elif operation == "remove":
                if target_line <= 0 or target_line > len(lines):
                    return create_error_result(f"Invalid line number: {target_line}")
                lines.pop(target_line - 1)
            else:
                return create_error_result(f"Unknown operation: {operation}")

        # Atomic write
        tmp = target.with_suffix(".tmp")
        tmp.write_text("".join(lines), encoding="utf-8")
        tmp.replace(target)

        return create_text_result(f"Patch applied to: {path}")
    except Exception as e:
        return create_error_result(f"Patch failed: {e}")


async def handle_git_status(arguments: dict[str, Any]) -> CallToolResult:
    """Get git status."""
    try:
        git = GitService(BRAIN_ROOT)
        status = git.get_status()
        return create_text_result(status if status else "Working tree clean")
    except Exception as e:
        return create_error_result(f"Git status failed: {e}")


async def handle_git_diff(arguments: dict[str, Any]) -> CallToolResult:
    """Get git diff."""
    try:
        path = arguments.get("path")
        git = GitService(BRAIN_ROOT)
        diff = git.get_diff(path)
        return create_text_result(diff if diff else "No changes")
    except Exception as e:
        return create_error_result(f"Git diff failed: {e}")


async def handle_git_log(arguments: dict[str, Any]) -> CallToolResult:
    """Get git log."""
    try:
        limit = arguments.get("limit", 10)
        git = GitService(BRAIN_ROOT)
        log = git.get_log(limit)
        return create_text_result(log)
    except Exception as e:
        return create_error_result(f"Git log failed: {e}")


async def handle_git_commit(arguments: dict[str, Any]) -> CallToolResult:
    """Create a git commit."""
    try:
        message = arguments.get("message", "")
        paths = arguments.get("paths", [])

        if not message:
            return create_error_result("Commit message is required")
        if not message.startswith("brain:"):
            return create_error_result("Commit message must start with 'brain:'")
        if not paths:
            return create_error_result("At least one path is required")

        git = GitService(BRAIN_ROOT)
        result = git.commit(message, paths)
        return create_text_result(result)
    except FileNotFoundError as e:
        return create_error_result(str(e))
    except Exception as e:
        return create_error_result(f"Git commit failed: {e}")


TOOL_HANDLERS = {
    "read_brain": handle_read_brain,
    "search_brain": handle_search_brain,
    "list_documents": handle_list_documents,
    "get_context": handle_get_context,
    "create_document": handle_create_document,
    "update_document": handle_update_document,
    "append_document": handle_append_document,
    "delete_document": handle_delete_document,
    "move_document": handle_move_document,
    "apply_patch": handle_apply_patch,
    "git_status": handle_git_status,
    "git_diff": handle_git_diff,
    "git_log": handle_git_log,
    "git_commit": handle_git_commit,
}