## 🧰 1. Create and Load a Virtual Environment with `uv`

From your terminal:

```bash
uv venv .venv
```

> This creates a virtual environment in the `.venv` directory using `uv`.

To **activate the virtual environment**:

### On Linux/macOS:

```bash
source .venv/bin/activate
```

### On Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

---

## 📦 2. Install `fastmcp`

Once the virtual environment is activated, run:

```bash
uv pip install fastmcp
```

---

## 🛠️ 3. Create the MCP Server – `nmap_mcp_server.py`

Create a file named `nmap_mcp_server.py` with the following content:

```python
# nmap_mcp_server.py

from fastmcp import FastMCP
from fastmcp.transports.uv import uv_run

mcp = FastMCP("Nmap MCP Server")

@mcp.tool
def nmap_scan(ip: str) -> str:
    # This is a mock, replace with real scanning logic if needed
    return f"Simulated scan results for {ip}"

if __name__ == "__main__":
    uv_run(mcp, host="127.0.0.1", port=8000)
```

---

## 🚀 4. Run the Server

In your terminal, while inside the virtual environment:

```bash
python nmap_mcp_server.py
```

You’ll see the server start up on `http://127.0.0.1:8000`.

---

## 🧪 5. Optional: Create a Client to Call the Tool

```python
# client.py

import asyncio
from fastmcp import Client

client = Client("http+uv://127.0.0.1:8000")

async def run():
    async with client:
        result = await client.call_tool("nmap_scan", {"ip": "192.168.1.1"})
        print(result)

asyncio.run(run())
```

Then run:

```bash
python client.py
```

Expected output:

```
Simulated scan results for 192.168.1.1
```


# 📘 FastMCP Tutorial: **Part 2 — Building a Nmap MCP Server with `uv`**

## ✅ What You'll Build

A running MCP server called `nmap_mcp_server` that includes:

* Local network discovery
* Quick and full Nmap scans
* Port, service, OS detection
* Script-based scanning
* Ping sweeps

---

## 📦 Step 1: Set Up Your Environment

### Create and activate a virtual environment:

```bash
uv venv .venv
source .venv/bin/activate  # Or `.venv\Scripts\Activate.ps1` on Windows
```

### Install FastMCP:

```bash
uv pip install fastmcp
```

Make sure `nmap` is installed on your system:

```bash
nmap --version
```

---

## 🛠 Step 2: Create the Nmap MCP Server

Create a new file called `nmap_mcp_server.py` and paste the following code:

```python
from fastmcp import FastMCP
from fastmcp.transports.uv import uv_run

import subprocess
import shlex
import socket
import re
import openai
import json

openai.api_key = "sk-..."  # Replace with your key or load from environment

mcp = FastMCP("Nmap MCP Server")


# === Nmap Utilities ===

def nmap_scan(target, options="", use_sudo=False):
    cmd_parts = []
    if use_sudo or any(f in options for f in ["-O", "-sS", "-sU", "--privileged"]):
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


# === FastMCP Tools ===

@mcp.tool
def nmap_quick_scan(target: str) -> str:
    return nmap_scan(target, "-T4 -F")


@mcp.tool
def nmap_port_scan(target: str, ports: str) -> str:
    return nmap_scan(target, f"-p {ports}")


@mcp.tool
def nmap_service_detection(target: str, ports: str = "") -> str:
    opts = "-sV"
    if ports:
        opts += f" -p {ports}"
    return nmap_scan(target, opts)


@mcp.tool
def nmap_os_detection(target: str) -> str:
    return nmap_scan(target, "-O", use_sudo=True)


@mcp.tool
def nmap_ping_scan(target: str) -> str:
    return nmap_scan(target, "-sn")


@mcp.tool
def nmap_script_scan(target: str, script: str, ports: str = "") -> str:
    opts = f"--script {script}"
    if ports:
        opts += f" -p {ports}"
    return nmap_scan(target, opts)


@mcp.tool
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

    return f"Hostname: {hostname}\nPrimary IP: {primary_ip}\nSuggested scan: {primary_ip.rsplit('.', 1)[0]}.0/24"


# === LLM Dispatcher Tool ===

@mcp.tool
async def natural_language_query(prompt: str) -> str:
    """
    Accepts a natural language prompt like:
    "Scan common ports on scanme.nmap.org"
    """
    system = """
You are a FastMCP tool router. Translate user prompts into structured tool calls.
Respond ONLY in this format:
{"tool": "tool_name", "params": {"arg1": "value", ...}}

Available tools:
- nmap_quick_scan(target)
- nmap_port_scan(target, ports)
- nmap_service_detection(target, ports)
- nmap_os_detection(target)
- nmap_ping_scan(target)
- nmap_script_scan(target, script, ports)
- get_local_network_info()
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    )

    try:
        result = json.loads(response["choices"][0]["message"]["content"])
        tool = result["tool"]
        params = result["params"]
        print(f"Dispatching: {tool}({params})")
        return await mcp.call_tool(tool, params)
    except Exception as ex:
        return f"Failed to interpret prompt: {ex}"


# === Run the MCP Server ===

if __name__ == "__main__":
    uv_run(mcp, host="127.0.0.1", port=18801)
```

---

## 🚀 Step 3: Run the Server

```bash
python nmap_mcp_server.py
```

This will start the MCP server on `http://127.0.0.1:18801`.

---

## 🧪 Step 4: Test It with a Client

Create a test file named `client.py`:

```python
import asyncio
from fastmcp import Client

client = Client("http+uv://127.0.0.1:18801")

async def test():
    async with client:
        result = await client.call_tool("nmap_quick_scan", {"target": "scanme.nmap.org"})
        print(result)

asyncio.run(test())
```

Then run:

```bash
python client.py
```

---

## 🧰 Available Tools

| Tool                                      | Description                      |
| ----------------------------------------- | -------------------------------- |
| `get_local_network_info()`                | Get local IPs and CIDR ranges    |
| `nmap_quick_scan(target)`                 | Fast scan on common ports        |
| `nmap_port_scan(target, ports)`           | Scan specific ports              |
| `nmap_service_detection(target, ports)`   | Detect running services          |
| `nmap_os_detection(target)`               | Detect target OS (requires sudo) |
| `nmap_ping_scan(target)`                  | Find live hosts via ping         |
| `nmap_script_scan(target, script, ports)` | Run Nmap scripts (e.g., `vuln`)  |
| `nmap_full_scan(target, options)`         | Custom Nmap command              |

---



