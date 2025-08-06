# my_uv_server.py

from fastmcp import FastMCP
from fastmcp.transports.uv import uv_run

mcp = FastMCP("My UV MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello from UV, {name}!"

@mcp.tool
def nmap_scan(ip: str) -> str:
    # This is a mock, replace with real scanning logic if needed
    return f"Simulated scan results for {ip}"

if __name__ == "__main__":
    uv_run(mcp, host="127.0.0.1", port=18800)

