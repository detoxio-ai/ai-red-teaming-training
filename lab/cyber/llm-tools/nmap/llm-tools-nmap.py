import llm
import subprocess
import shlex
import socket
import re


def get_local_network_info():
    """
    Get local network information including IP addresses, subnet masks, and network ranges for scanning.
    
    Returns:
        A string containing local IP addresses, subnet information, and suggested scan ranges
    """
    try:
        # Get hostname
        hostname = socket.gethostname()
        
        # Method 1: Get IP by connecting to a public DNS server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Connect to Google's public DNS server
            s.connect(("8.8.8.8", 80))
            primary_ip = s.getsockname()[0]
            s.close()
        except:
            primary_ip = "Unable to determine"
        
        # Method 2: Get all IPs associated with hostname
        try:
            all_ips = socket.gethostbyname_ex(hostname)[2]
        except:
            all_ips = []
        
        # Try to get network interface information using ip command (Linux/macOS)
        interface_info = []
        scan_ranges = []
        
        try:
            result = subprocess.run(
                ["ip", "addr", "show"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # Parse output for interface names and IPs
                current_interface = None
                for line in result.stdout.split('\n'):
                    # Match interface line
                    if re.match(r'^\d+:', line):
                        current_interface = line.split(':')[1].strip()
                    # Match inet line
                    elif 'inet ' in line and current_interface:
                        ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/(\d+)', line)
                        if ip_match and not ip_match.group(1).startswith('127.'):
                            ip_addr = ip_match.group(1)
                            cidr = ip_match.group(2)
                            interface_info.append(f"{current_interface}: {ip_addr}/{cidr}")
                            
                            # Calculate network range
                            network_range = calculate_network_range(ip_addr, cidr)
                            if network_range and network_range not in scan_ranges:
                                scan_ranges.append(network_range)
        except:
            # If ip command fails, try ifconfig
            try:
                result = subprocess.run(
                    ["ifconfig"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    # Parse ifconfig output for interfaces
                    current_interface = None
                    lines = result.stdout.split('\n')
                    
                    for i, line in enumerate(lines):
                        # Detect interface name (starts at beginning of line)
                        if line and not line.startswith(' ') and not line.startswith('\t'):
                            current_interface = line.split()[0].rstrip(':')
                        
                        # Look for inet lines
                        if 'inet ' in line and current_interface:
                            # Extract IP
                            ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', line)
                            if ip_match and not ip_match.group(1).startswith('127.'):
                                ip_addr = ip_match.group(1)
                                
                                # Try to find netmask
                                netmask_match = re.search(r'netmask (\d+\.\d+\.\d+\.\d+)', line)
                                if netmask_match:
                                    netmask = netmask_match.group(1)
                                    cidr = netmask_to_cidr(netmask)
                                    interface_info.append(f"{current_interface}: {ip_addr}/{cidr}")
                                    
                                    # Calculate network range
                                    network_range = calculate_network_range(ip_addr, str(cidr))
                                    if network_range and network_range not in scan_ranges:
                                        scan_ranges.append(network_range)
                                else:
                                    interface_info.append(f"{current_interface}: {ip_addr}")
            except:
                pass
        
        # Build response
        response = f"Hostname: {hostname}\n"
        response += f"Primary IP: {primary_ip}\n"
        
        if all_ips:
            response += f"All IPs for hostname: {', '.join(all_ips)}\n"
        
        if interface_info:
            response += "\nNetwork interfaces:\n"
            for info in interface_info:
                response += f"  {info}\n"
        
        if scan_ranges:
            response += "\nNetwork ranges (for scanning):\n"
            for range_info in scan_ranges:
                response += f"  {range_info}\n"
        else:
            # Fallback: suggest /24 network if we have a primary IP
            if primary_ip != "Unable to determine":
                octets = primary_ip.split('.')
                if len(octets) == 4:
                    network_base = f"{octets[0]}.{octets[1]}.{octets[2]}.0/24"
                    response += f"\nSuggested scan range (assuming /24): {network_base}\n"
        
        # Add helpful note
        response += "\nNote: Use the network ranges above with nmap_ping_scan to discover all devices."
        
        return response
        
    except Exception as ex:
        return f"Error getting network info: {type(ex).__name__}: {ex}"


def calculate_network_range(ip_addr, cidr):
    """Calculate network range from IP and CIDR notation"""
    try:
        cidr_int = int(cidr)
        # Calculate network address
        ip_parts = [int(x) for x in ip_addr.split('.')]
        
        # Calculate host bits
        host_bits = 32 - cidr_int
        
        # Create subnet mask
        mask = (0xFFFFFFFF << host_bits) & 0xFFFFFFFF
        
        # Calculate network address
        network_addr = []
        for i in range(4):
            network_addr.append(ip_parts[i] & ((mask >> (24 - i * 8)) & 0xFF))
        
        network_str = '.'.join(map(str, network_addr))
        return f"{network_str}/{cidr}"
    except:
        return None


def netmask_to_cidr(netmask):
    """Convert netmask to CIDR notation"""
    try:
        # Convert netmask to binary and count the 1s
        parts = netmask.split('.')
        binary = ''.join([bin(int(part))[2:].zfill(8) for part in parts])
        return binary.count('1')
    except:
        return 24  # Default to /24


def nmap_scan(target, options="", use_sudo=False):  # Default use_sudo is False
    """
    Run an Nmap scan on the specified target with optional parameters.

    Args:
        target: The target to scan (IP address, hostname, or IP range)
        options: Additional Nmap command line options (e.g., "-sS -p 80,443")
        use_sudo: Whether to use sudo for privileged scans

    Returns:
        The output of the Nmap scan
    """
    cmd_parts = []

    privileged_flags = ["-O", "-sS", "-sU", "--privileged"]
    if use_sudo or any(flag in options for flag in privileged_flags):
        cmd_parts.append("sudo")  # Add sudo if explicitly requested or implied

    cmd_parts.append("nmap")

    if options:
        cmd_parts.extend(shlex.split(options))

    cmd_parts.append(target)

    try:
        result = subprocess.run(
            cmd_parts,
            capture_output=True,
            text=True,
            timeout=300,
            check=False
        )

        if result.returncode != 0:
            return f"Error: Nmap returned non-zero exit code {result.returncode}\nStderr: {result.stderr}"

        return result.stdout

    except subprocess.TimeoutExpired:
        return "Error: Nmap scan timed out after 5 minutes"
    except FileNotFoundError:
        return "Error: nmap command not found. Please install nmap first."
    except Exception as ex:
        return f"Error: {type(ex).__name__}: {ex}"

def nmap_quick_scan(target):
    """
    Perform a quick Nmap scan on common ports with faster timing.

    Args:
        target (str): The IP address, hostname, or range to scan.

    Returns:
        str: Output of the Nmap quick scan.
    """
    return nmap_scan(target, "-T4 -F")


def nmap_port_scan(target, ports):
    """
    Scan specific ports on the given target.

    Args:
        target (str): The IP address or hostname to scan.
        ports (str): Port specification string (e.g., "80", "22,443", "1-1000").

    Returns:
        str: Output of the Nmap port scan.
    """
    return nmap_scan(target, f"-p {ports}")


def nmap_service_detection(target, ports=""):
    """
    Detect service versions running on target ports.

    Args:
        target (str): The target IP or hostname.
        ports (str, optional): Port list to scan. If omitted, default ports are used.

    Returns:
        str: Nmap output with service version information.
    """
    options = "-sV"
    if ports:
        options += f" -p {ports}"
    return nmap_scan(target, options)


def nmap_os_detection(target):
    """
    Attempt to detect the operating system of the target host.
    Requires sudo privileges to send raw packets.

    Args:
        target (str): The IP address or hostname of the target.

    Returns:
        str: Nmap output including OS guess and network distance.
    """
    return nmap_scan(target, "-O", use_sudo=True)


def nmap_ping_scan(target):
    """
    Perform a ping-only scan to discover live hosts in a network.
    No ports are scanned.

    Args:
        target (str): CIDR range or IP (e.g., "192.168.1.0/24").

    Returns:
        str: List of live hosts detected by Nmap.
    """
    return nmap_scan(target, "-sn")


def nmap_script_scan(target, script, ports=""):
    """
    Run a specified Nmap script (or script category) against a target.

    Args:
        target (str): The IP address or hostname to scan.
        script (str): Name or category of the script (e.g., "http-title", "vuln").
        ports (str, optional): Ports to run the script against.

    Returns:
        str: Output of the Nmap script scan.
    """
    options = f"--script {script}"
    if ports:
        options += f" -p {ports}"
    return nmap_scan(target, options)


@llm.hookimpl
def register_tools(register):
    # Register each function as a separate tool
    register(get_local_network_info)
    register(nmap_scan)
    register(nmap_quick_scan)
    register(nmap_port_scan)
    register(nmap_service_detection)
    register(nmap_os_detection)
    register(nmap_ping_scan)
    register(nmap_script_scan)
