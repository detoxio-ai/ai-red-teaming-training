import llm
import subprocess
import shlex
import socket
import re


def check_vulnerability_with_metasploit(target, port, module_path):
    """
    Use a Metasploit module to check if a service on the target is vulnerable.
    
    Args:
        target (str): IP of the host.
        port (int): Port the service is running on.
        module_path (str): Metasploit module path (e.g., 'exploit/linux/redis/...').
    
    Returns:
        str: Output from the Metasploit 'check' command.
    """
    try:
        rc_script = f"""
use {module_path}
set RHOSTS {target}
set RPORT {port}
set ExitOnSession false
check
exit
"""
        rc_file_path = "/tmp/metasploit_check.rc"
        with open(rc_file_path, "w") as f:
            f.write(rc_script)

        result = subprocess.run(
            ["msfconsole", "-q", "-r", rc_file_path],
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.stdout
    except FileNotFoundError:
        return "Error: msfconsole not found. Please install Metasploit."
    except subprocess.TimeoutExpired:
        return "Error: Metasploit check timed out."
    except Exception as ex:
        return f"Error: {type(ex).__name__}: {ex}"

import subprocess
import re

def find_metasploit_modules_for_service(target, service, ports=None):
    """
    Scan the target for the given service and search for related Metasploit modules.

    Args:
        target (str): IP or hostname to scan.
        service (str): Service name to filter (e.g., 'redis', 'ftp').
        ports (str, optional): Comma-separated list or range of ports to scan (e.g., "21,22,6379" or "1-1000").

    Returns:
        dict: {
            "open_ports": [<port numbers>],
            "metasploit_modules": [<module lines>]
            "nmap_result": [<result lines>]
        }
    """
    open_ports = []
    msf_modules = []

    try:
        print(f"[+] Running Nmap service scan on {target} for service '{service}'...")

        # Build the nmap command
        nmap_cmd = ["nmap", "-sV", "-Pn", "--open"]
        if ports:
            nmap_cmd.extend(["-p", ports])
        nmap_cmd.append(target)

        result = subprocess.run(nmap_cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            return {"error": "Nmap scan failed", "details": result.stderr}

        # Extract open ports matching the service
        nmap_result = []
        for line in result.stdout.splitlines():
            nmap_result.append(line)
            match = re.search(r"(\d{1,5})/tcp\s+open\s+([^\s]+)", line)
            if match:
                port, detected_service = match.groups()
                print(f"[DEBUG] Detected service '{detected_service}' on port {port}")
                if service.lower() in detected_service.lower():
                    open_ports.append(int(port))

        if not open_ports:
            return {
                "open_ports": [],
                "metasploit_modules": [],
                "note": f"No open ports found for service '{service}' on target {target}"
            }

        print(f"[+] Found open ports for {service}: {open_ports}")

        # Search for Metasploit modules
        print(f"[+] Searching Metasploit modules for '{service}'...")
        msf_cmd = ["msfconsole", "--quiet", "-x", f"search {service}; exit"]
        msf_result = subprocess.run(msf_cmd, capture_output=True, text=True, timeout=60)

        # Debug raw Metasploit output
        print("[DEBUG] Raw Metasploit search output:")
        #print(msf_result.stdout)

        for line in msf_result.stdout.splitlines():
            msf_modules.append(line.strip())

        return {
            "open_ports": open_ports,
            "metasploit_modules": msf_modules if msf_modules else ["[No modules found]"],
            "nmap_scan": nmap_result
        }

    except subprocess.TimeoutExpired:
        return {"error": "Timeout expired during scanning or searching"}
    except FileNotFoundError as e:
        return {"error": f"Missing tool: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}



@llm.hookimpl
def register_tools(register):
    # Register each function as a separate tool
    register(find_metasploit_modules_for_service)
    register(check_vulnerability_with_metasploit)
