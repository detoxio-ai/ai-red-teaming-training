
from fastmcp import FastMCP

mcp = FastMCP("My UV MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello from UV, {name}!"


