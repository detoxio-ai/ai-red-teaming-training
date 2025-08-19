from fastmcp import FastMCP
import subprocess
import shlex
import socket
import openai
import json


# === Create MCP Server ===
mcp = FastMCP("Nmap MCP Server")


# === Nmap Utility ===
def nmap_scan(target, options="", use_sudo=False):
    cmd_parts = []
    if use_sudo or any(opt in options for opt in ["-O", "-sS", "-sU", "--privileged"]):
        cmd_parts.append("sudo")
    cmd_parts.append("nmap")
    if options:
        cmd_parts.extend(shlex.split(options))
    cmd_parts.append(target)

    try:
        result = subprocess.run(cmd_parts, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            return f"Error: Nmap returned code {result.returncode}\n{result.stderr}"
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Scan timed out"
    except Exception as ex:
        return f"Error: {type(ex).__name__}: {ex}"


# === Registered MCP Tools ===

@mcp.tool(description="Returns a friendly greeting.")
def greet(name: str) -> str:
    return f"Hello, {name}!"


@mcp.tool(description="Quick Nmap scan using fast timing and top ports.")
def nmap_quick_scan(target: str) -> str:
    return nmap_scan(target, "-T4 -F")


@mcp.tool(description="Scan specific ports on a target.")
def nmap_port_scan(target: str, ports: str) -> str:
    return nmap_scan(target, f"-p {ports}")


@mcp.tool(description="Detect services running on specified ports.")
def nmap_service_detection(target: str, ports: str = "") -> str:
    opts = "-sV"
    if ports:
        opts += f" -p {ports}"
    return nmap_scan(target, opts)


@mcp.tool(description="Detect operating system of the target (requires sudo).")
def nmap_os_detection(target: str) -> str:
    return nmap_scan(target, "-O", use_sudo=True)


@mcp.tool(description="Ping scan to detect live hosts.")
def nmap_ping_scan(target: str) -> str:
    return nmap_scan(target, "-sn")


@mcp.tool(description="Run specific Nmap scripts on a target and ports.")
def nmap_script_scan(target: str, script: str, ports: str = "") -> str:
    opts = f"--script {script}"
    if ports:
        opts += f" -p {ports}"
    return nmap_scan(target, opts)


@mcp.tool(description="Get hostname, local IP, and a suggested subnet for scanning.")
def get_local_network_info() -> str:
    hostname = socket.gethostname()
    primary_ip = "unknown"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        primary_ip = s.getsockname()[0]
        s.close()
    except:
        pass

    subnet = f"{primary_ip.rsplit('.', 1)[0]}.0/24" if primary_ip != "unknown" else "unknown"
    return f"Hostname: {hostname}\nPrimary IP: {primary_ip}\nSuggested scan: {subnet}"


@mcp.tool(description="Run a custom Nmap command with arbitrary options.")
def nmap_custom_scan(target: str, options: str = "", use_sudo: bool = False) -> str:
    return nmap_scan(target, options, use_sudo=use_sudo)


# === LLM Dispatcher Tool ===

@mcp.tool(description="Process a natural language query and dispatch to the appropriate tool.")
async def natural_language_query(prompt: str) -> str:
    system = """
You are a FastMCP tool router. Translate user prompts into structured tool calls.
Respond ONLY in this format:
{"tool": "tool_name", "params": {"arg1": "value", ...}}

Available tools:
- greet(name)
- nmap_quick_scan(target)
- nmap_port_scan(target, ports)
- nmap_service_detection(target, ports)
- nmap_os_detection(target)
- nmap_ping_scan(target)
- nmap_script_scan(target, script, ports)
- nmap_custom_scan(target, options, use_sudo)
- get_local_network_info()
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ]
        )
        content = response["choices"][0]["message"]["content"]
        result = json.loads(content)
        tool = result["tool"]
        params = result.get("params", {})

        if tool not in mcp.list_tools():
            return f"Tool '{tool}' is not registered."

        print(f"Dispatching: {tool}({params})")
        return await mcp.call_tool(tool, params)

    except json.JSONDecodeError as jde:
        return f"LLM returned invalid JSON: {jde}\nResponse: {content}"
    except Exception as ex:
        return f"Failed to interpret prompt: {ex}"

