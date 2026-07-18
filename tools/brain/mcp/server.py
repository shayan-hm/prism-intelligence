"""MCP Server entry point for Prism Brain."""

import asyncio
import logging

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

from tools.brain.mcp.tools import ALL_TOOLS
from tools.brain.mcp.handlers import TOOL_HANDLERS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BrainMCPServer:
    """MCP Server exposing Brain tools."""

    def __init__(self):
        self.server = Server("prism-brain")
        self._register_tools()

    def _register_tools(self) -> None:
        """Register all tools with the server."""

        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            return ALL_TOOLS

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> list:
            handler = TOOL_HANDLERS.get(name)
            if not handler:
                raise ValueError(f"Unknown tool: {name}")
            return await handler(arguments)

    async def run(self) -> None:
        """Run the MCP server over stdio."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main() -> None:
    """Main entry point."""
    server = BrainMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())