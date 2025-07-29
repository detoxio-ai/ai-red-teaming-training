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


def nmap_scan(target, options=""):
    """
    Run an Nmap scan on the specified target with optional parameters.
    
    Args:
        target: The target to scan (IP address, hostname, or IP range)
        options: Additional Nmap command line options (e.g., "-sS -p 80,443")
    
    Returns:
        The output of the Nmap scan
    """
    # Build the command
    cmd_parts = ["nmap"]
    
    # Add options if provided
    if options:
        # Use shlex to safely split the options string
        cmd_parts.extend(shlex.split(options))
    
    # Add the target
    cmd_parts.append(target)
    
    try:
        # Run the command
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
    """
    Run an Nmap scan on the specified target with optional parameters.
    
    Args:
        target: The target to scan (IP address, hostname, or IP range)
        options: Additional Nmap command line options (e.g., "-sS -p 80,443")
    
    Returns:
        The output of the Nmap scan
    """
    # Build the command
    cmd_parts = ["nmap"]
    
    # Add options if provided
    if options:
        # Use shlex to safely split the options string
        cmd_parts.extend(shlex.split(options))
    
    # Add the target
    cmd_parts.append(target)
    
    try:
        # Run the command
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
    Perform a quick TCP scan on the most common ports.
    Equivalent to: nmap -T4 -F target
    
    Args:
        target: The target to scan
    
    Returns:
        The output of the quick scan
    """
    return nmap_scan(target, "-T4 -F")


def nmap_port_scan(target, ports):
    """
    Scan specific ports on the target.
    
    Args:
        target: The target to scan
        ports: Port specification (e.g., "80", "80,443", "1-1000", "U:53,T:80")
    
    Returns:
        The output of the port scan
    """
    return nmap_scan(target, f"-p {ports}")


def nmap_service_detection(target, ports=""):
    """
    Perform service version detection on the target.
    
    Args:
        target: The target to scan
        ports: Optional port specification (if not provided, scans default ports)
    
    Returns:
        The output with service detection results
    """
    options = "-sV"
    if ports:
        options += f" -p {ports}"
    return nmap_scan(target, options)


def nmap_os_detection(target):
    """
    Attempt to detect the operating system of the target.
    Note: This typically requires root/sudo privileges.
    
    Args:
        target: The target to scan
    
    Returns:
        The output with OS detection results
    """
    return nmap_scan(target, "-O")


def nmap_ping_scan(target):
    """
    Perform a ping scan to discover live hosts (no port scanning).
    
    Args:
        target: The target or range to scan (e.g., "192.168.1.0/24")
    
    Returns:
        The list of live hosts
    """
    return nmap_scan(target, "-sn")


def nmap_script_scan(target, script, ports=""):
    """
    Run a specific Nmap script against the target.
    
    Args:
        target: The target to scan
        script: The script name or category (e.g., "http-title", "vuln")
        ports: Optional port specification
    
    Returns:
        The output of the script scan
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
