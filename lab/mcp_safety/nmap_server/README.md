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

mcp = FastMCP("Nmap MCP Server")


@mcp.tool
def get_local_network_info() -> str:
    # Discover local IPs, interfaces, and CIDR scan ranges
    try:
        hostname = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            primary_ip = s.getsockname()[0]
            s.close()
        except:
            primary_ip = "Unable to determine"

        try:
            all_ips = socket.gethostbyname_ex(hostname)[2]
        except:
            all_ips = []

        interface_info = []
        scan_ranges = []

        try:
            result = subprocess.run(["ip", "addr", "show"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                current_interface = None
                for line in result.stdout.split('\n'):
                    if re.match(r'^\d+:', line):
                        current_interface = line.split(':')[1].strip()
                    elif 'inet ' in line and current_interface:
                        ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/(\d+)', line)
                        if ip_match and not ip_match.group(1).startswith('127.'):
                            ip_addr = ip_match.group(1)
                            cidr = ip_match.group(2)
                            interface_info.append(f"{current_interface}: {ip_addr}/{cidr}")
                            network_range = calculate_network_range(ip_addr, cidr)
                            if network_range and network_range not in scan_ranges:
                                scan_ranges.append(network_range)
        except:
            pass

        response = f"Hostname: {hostname}\nPrimary IP: {primary_ip}\n"
        if all_ips:
            response += f"All IPs for hostname: {', '.join(all_ips)}\n"
        if interface_info:
            response += "\nNetwork interfaces:\n" + '\n'.join(f"  {info}" for info in interface_info)
        if scan_ranges:
            response += "\n\nNetwork ranges:\n" + '\n'.join(f"  {r}" for r in scan_ranges)
        else:
            if primary_ip != "Unable to determine":
                octets = primary_ip.split('.')
                if len(octets) == 4:
                    response += f"\nSuggested scan range: {octets[0]}.{octets[1]}.{octets[2]}.0/24\n"

        response += "\nUse this info with nmap_ping_scan to discover live hosts."
        return response
    except Exception as ex:
        return f"Error: {type(ex).__name__}: {ex}"


def calculate_network_range(ip_addr, cidr):
    try:
        cidr_int = int(cidr)
        ip_parts = [int(x) for x in ip_addr.split('.')]
        host_bits = 32 - cidr_int
        mask = (0xFFFFFFFF << host_bits) & 0xFFFFFFFF
        network_addr = [(ip_parts[i] & ((mask >> (24 - i * 8)) & 0xFF)) for i in range(4)]
        return f"{'.'.join(map(str, network_addr))}/{cidr}"
    except:
        return None


def nmap_scan(target, options="", use_sudo=False):
    cmd_parts = []
    privileged_flags = ["-O", "-sS", "-sU", "--privileged"]
    if use_sudo or any(flag in options for flag in privileged_flags):
        cmd_parts.append("sudo")
    cmd_parts.append("nmap")
    if options:
        cmd_parts.extend(shlex.split(options))
    cmd_parts.append(target)
    try:
        result = subprocess.run(cmd_parts, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            return f"Error: Nmap exited with code {result.returncode}\nStderr: {result.stderr}"
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Error: Scan timed out"
    except FileNotFoundError:
        return "Error: Nmap not installed"
    except Exception as ex:
        return f"Error: {type(ex).__name__}: {ex}"


@mcp.tool
def nmap_quick_scan(target: str) -> str:
    return nmap_scan(target, "-T4 -F")


@mcp.tool
def nmap_port_scan(target: str, ports: str) -> str:
    return nmap_scan(target, f"-p {ports}")


@mcp.tool
def nmap_service_detection(target: str, ports: str = "") -> str:
    options = "-sV"
    if ports:
        options += f" -p {ports}"
    return nmap_scan(target, options)


@mcp.tool
def nmap_os_detection(target: str) -> str:
    return nmap_scan(target, "-O", use_sudo=True)


@mcp.tool
def nmap_ping_scan(target: str) -> str:
    return nmap_scan(target, "-sn")


@mcp.tool
def nmap_script_scan(target: str, script: str, ports: str = "") -> str:
    options = f"--script {script}"
    if ports:
        options += f" -p {ports}"
    return nmap_scan(target, options)


@mcp.tool
def nmap_full_scan(target: str, options: str = "") -> str:
    return nmap_scan(target, options)


if __name__ == "__main__":
    uv_run(mcp, host="127.0.0.1", port=8000)
```

---

## 🚀 Step 3: Run the Server

```bash
python nmap_mcp_server.py
```

This will start the MCP server on `http://127.0.0.1:8000`.

---

## 🧪 Step 4: Test It with a Client

Create a test file named `client.py`:

```python
import asyncio
from fastmcp import Client

client = Client("http+uv://127.0.0.1:8000")

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



