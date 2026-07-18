# Prism Brain Access Layer & MCP Server

## Purpose

The Brain Access Layer provides a secure, type-safe interface for reading, writing, and searching the `brain/` knowledge repository. It includes a production-ready MCP (Model Context Protocol) server for AI agent integration.

## Architecture

```
tools/brain/
├── server.py              # MCP server entry point
├── config.py              # Centralized configuration (paths)
├── exceptions.py          # Custom exception hierarchy
├── models.py              # Data models (dataclasses)
├── registry.py            # Service factory / singleton access
├── services/
│   ├── reader.py          # Secure file reading with path traversal protection
│   ├── search.py          # Full-text search across markdown files
│   ├── context.py         # Multi-document context assembly
│   ├── manifest.py        # Document discovery and metadata
│   └── patch.py           # Patch interface (not yet implemented)
├── mcp/
│   ├── __init__.py        # Package exports
│   ├── server.py          # MCP server implementation
│   ├── tools.py           # Tool definitions (14 tools)
│   ├── handlers.py        # Tool handlers (delegates to services)
│   └── transport.py       # stdio transport
├── git/
│   ├── __init__.py        # Package exports
│   └── service.py         # Git operations wrapper
└── tests/
    ├── test_reader.py     # Reader unit tests
    ├── test_mcp.py        # MCP handler tests
    └── test_git.py        # Git service tests
```

## Responsibilities

| Layer | Service | Responsibility |
|-------|---------|----------------|
| **Access** | `reader.py` | Read single markdown files with security validation |
| **Access** | `search.py` | Case-insensitive search across all `*.md` files |
| **Access** | `context.py` | Concatenate multiple documents with filename headers |
| **Access** | `manifest.py` | Discover all documents with title and modification time |
| **Access** | `patch.py` | Interface for future write operations |
| **MCP** | `handlers.py` | Delegates tool calls to existing services |
| **MCP** | `tools.py` | 14 MCP tool definitions |
| **Git** | `service.py` | Thin wrapper for git operations |

## Available MCP Tools

### Brain Tools (Read)

| Tool | Description | Parameters |
|------|-------------|------------|
| `read_brain` | Read a markdown file | `path: string` |
| `search_brain` | Search across all markdown files | `query: string` |
| `list_documents` | List all documents with metadata | (none) |
| `get_context` | Concatenate multiple files | `paths: string[]` |

### Brain Tools (Write)

| Tool | Description | Parameters |
|------|-------------|------------|
| `create_document` | Create new markdown file | `path, content, title?` |
| `update_document` | Full replace of existing file | `path, content` |
| `append_document` | Append to existing file | `path, content, separator?` |
| `delete_document` | Delete a markdown file | `path` |
| `move_document` | Move/rename a file | `source, destination` |
| `apply_patch` | Line-based patch operations | `path, operations[]` |

### Git Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `git_status` | Show git status for brain/ | (none) |
| `git_diff` | Show git diff | `path?` |
| `git_log` | Show recent commits | `limit? (default: 10)` |
| `git_commit` | Stage and commit files | `message, paths[]` |

## Security

- All file access is restricted to `brain/` directory
- Path traversal attempts raise `BrainSecurityError`
- Only `.md` files are accessible
- Hidden files/directories (starting with `.`) are ignored
- Atomic writes using temp file + rename
- Parent directories created automatically
- Symlinks are resolved and validated against brain root

## Running the MCP Server

```bash
# Run directly
python -m tools.brain.mcp.server

# Or via the package entry point (if configured)
prism-brain-mcp
```

The server communicates over stdio and is designed to be launched by an MCP client (e.g., Claude Desktop, Cursor, etc.).

### MCP Client Configuration (Claude Desktop)

```json
{
  "mcpServers": {
    "prism-brain": {
      "command": "python",
      "args": ["-m", "tools.brain.mcp.server"],
      "cwd": "/path/to/prism-intelligence"
    }
  }
}
```

## Usage (Python API)

```python
from tools.brain.registry import get_reader, get_search, get_context, get_manifest

# Read a single document
content = get_reader()("knowledge/decisions/adr-001-twr-metric.md")

# Search across all documents
results = get_search()("risk management")

# Build context from multiple documents
context = get_context()([
    "knowledge/domains/risk.md",
    "knowledge/decisions/adr-002-strategy-context.md"
])

# Get document manifest
documents = get_manifest()()
for doc in documents:
    print(f"{doc.relative_path}: {doc.title}")
```

## Write Operations

All write operations enforce:
- Path must be within `brain/` (traversal blocked)
- Only `.md` extension allowed
- Atomic writes via temp file + rename
- UTF-8 encoding
- Parent directories auto-created

```python
from tools.brain.mcp.handlers import handle_create_document, handle_update_document
import asyncio

# Create new document
asyncio.run(handle_create_document({
    "path": "knowledge/domains/new-topic.md",
    "content": "# New Topic\n\nContent here.",
    "title": "New Topic"
}))

# Update existing document
asyncio.run(handle_update_document({
    "path": "knowledge/domains/market.md",
    "content": "# Market\n\nUpdated content."
}))
```

## Git Integration

The git tools provide a thin wrapper around the repository:
- `git_status`: Shows modified/staged files in brain/
- `git_diff`: Shows diff for brain/ or specific file
- `git_log`: Shows recent commits (default 10)
- `git_commit`: Stages specified files and commits with "brain:" prefix

No automatic commits - all commits require explicit user action via `git_commit`.

## Future Extensions

- **Pull/Push**: Add `git_pull` and `git_push` tools for remote sync
- **Branch Management**: `git_branch`, `git_checkout` for multi-branch workflows
- **Patch v2**: Full unified diff support in `apply_patch`
- **Webhooks**: Notify on brain/ changes
- **Indexing**: Background search index for large repos
- **Authentication**: Token-based access for remote MCP clients