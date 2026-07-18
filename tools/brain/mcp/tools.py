"""MCP Tool definitions for Prism Brain."""

from mcp.types import Tool


# Brain tools
READ_TOOL = Tool(
    name="read_brain",
    description="Read a markdown file from the brain knowledge base",
    inputSchema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative path to the markdown file (e.g., 'knowledge/domains/market.md')"
            }
        },
        "required": ["path"]
    }
)

SEARCH_TOOL = Tool(
    name="search_brain",
    description="Search for text across all markdown files in the brain knowledge base",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query (case-insensitive)"
            }
        },
        "required": ["query"]
    }
)

CONTEXT_TOOL = Tool(
    name="get_context",
    description="Read multiple markdown files and concatenate them with filename headers",
    inputSchema={
        "type": "object",
        "properties": {
            "paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of relative paths to markdown files"
            }
        },
        "required": ["paths"]
    }
)

MANIFEST_TOOL = Tool(
    name="list_documents",
    description="List all markdown documents in the brain with metadata (path, title, last modified)",
    inputSchema={
        "type": "object",
        "properties": {}
    }
)

CREATE_TOOL = Tool(
    name="create_document",
    description="Create a new markdown document in the brain",
    inputSchema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative path for the new document (must end with .md)"
            },
            "content": {
                "type": "string",
                "description": "Markdown content for the document"
            },
            "title": {
                "type": "string",
                "description": "Optional title (will be added as H1)"
            }
        },
        "required": ["path"]
    }
)

UPDATE_TOOL = Tool(
    name="update_document",
    description="Update an existing brain document (full replace)",
    inputSchema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative path to the document"
            },
            "content": {
                "type": "string",
                "description": "New markdown content"
            }
        },
        "required": ["path", "content"]
    }
)

APPEND_TOOL = Tool(
    name="append_document",
    description="Append content to an existing brain document",
    inputSchema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative path to the document"
            },
            "content": {
                "type": "string",
                "description": "Content to append"
            },
            "separator": {
                "type": "string",
                "description": "Separator to add before appended content",
                "default": "\n\n---\n\n"
            }
        },
        "required": ["path", "content"]
    }
)

DELETE_TOOL = Tool(
    name="delete_document",
    description="Delete a brain document",
    inputSchema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative path to the document to delete"
            }
        },
        "required": ["path"]
    }
)

MOVE_TOOL = Tool(
    name="move_document",
    description="Move or rename a brain document",
    inputSchema={
        "type": "object",
        "properties": {
            "source": {
                "type": "string",
                "description": "Current relative path"
            },
            "destination": {
                "type": "string",
                "description": "New relative path"
            }
        },
        "required": ["source", "destination"]
    }
)

PATCH_TOOL = Tool(
    name="apply_patch",
    description="Apply line-based patches to a brain document",
    inputSchema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative path to the document"
            },
            "operations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "operation": {"type": "string", "enum": ["add", "replace", "remove"]},
                        "content": {"type": "string"},
                        "target_line": {"type": "integer"}
                    },
                    "required": ["operation", "content"]
                }
            }
        },
        "required": ["path", "operations"]
    }
)

# Git tools
GIT_STATUS_TOOL = Tool(
    name="git_status",
    description="Get the git status of the brain repository",
    inputSchema={
        "type": "object",
        "properties": {}
    }
)

GIT_DIFF_TOOL = Tool(
    name="git_diff",
    description="Get the git diff for brain files",
    inputSchema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Optional path to diff (relative to brain root)"
            }
        }
    }
)

GIT_LOG_TOOL = Tool(
    name="git_log",
    description="Get recent git log for brain files",
    inputSchema={
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Number of commits to show",
                "default": 10
            }
        }
    }
)

GIT_COMMIT_TOOL = Tool(
    name="git_commit",
    description="Create a git commit for brain changes (message must start with 'brain:')",
    inputSchema={
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Commit message (must start with 'brain:')"
            },
            "paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Paths to stage and commit"
            }
        },
        "required": ["message", "paths"]
    }
)


ALL_TOOLS = [
    READ_TOOL,
    SEARCH_TOOL,
    CONTEXT_TOOL,
    MANIFEST_TOOL,
    CREATE_TOOL,
    UPDATE_TOOL,
    APPEND_TOOL,
    DELETE_TOOL,
    MOVE_TOOL,
    PATCH_TOOL,
    GIT_STATUS_TOOL,
    GIT_DIFF_TOOL,
    GIT_LOG_TOOL,
    GIT_COMMIT_TOOL,
]