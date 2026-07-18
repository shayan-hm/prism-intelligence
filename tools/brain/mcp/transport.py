"""MCP transport for brain server."""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

from tools.brain.mcp.tools import ALL_TOOLS
from tools.brain.mcp.handlers import TOOL_HANDLERS, CallToolResult


def create_server() -> Server:
    """Create and configure the MCP server."""
    server = Server("prism-brain")

    # Register all tools
    for tool in ALL_TOOLS:
        server.add_tool(tool)

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> CallToolResult:
        """Route tool calls to handlers."""
        handler = TOOL_HANDLERS.get(name)
        if not handler:
            return CallToolResult(
                content=[{"type": "text", "text": f"Unknown tool: {name}"}],
                isError=True
            )
        return await handler(arguments)

    return server


async def run_server() -> None:
    """Run the MCP server over stdio."""
    server = create_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(run_server())