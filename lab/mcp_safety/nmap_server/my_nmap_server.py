# nmap_mcp_server.py

from fastmcp import FastMCP
import subprocess
import shlex

mcp = FastMCP("Nmap MCP Server")

def run_nmap_command(target: str, options: str) -> str:
    """Run an nmap command and return output or error."""
    cmd = ["nmap"] + shlex.split(options) + [target]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            return f"[Error {result.returncode}]\n{result.stderr}"
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Error: Nmap scan timed out."
    except FileNotFoundError:
        return "Error: Nmap is not installed or not in PATH."
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"

@mcp.tool
def ping_scan(target: str) -> str:
    """Ping scan to discover live hosts (nmap -sn)."""
    return run_nmap_command(target, "-sn")

@mcp.tool
def quick_scan(target: str) -> str:
    """Quick scan common ports (nmap -T4 -F)."""
    return run_nmap_command(target, "-T4 -F")

@mcp.tool
def port_scan(target: str, ports: str) -> str:
    """Scan specific ports (nmap -p)."""
    return run_nmap_command(target, f"-p {ports}")

@mcp.tool
def service_detection(target: str) -> str:
    """Service and version detection (nmap -sV)."""
    return run_nmap_command(target, "-sV")

@mcp.tool
def os_detection(target: str) -> str:
    """OS detection (nmap -O). Requires sudo privileges."""
    return run_nmap_command(target, "-O")

if __name__ == "__main__":
    mcp.run()

