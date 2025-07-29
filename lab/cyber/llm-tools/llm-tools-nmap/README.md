# LLM-Nmap

A plugin for [Simon Willison's LLM](https://llm.datasette.io/) tool that provides Nmap network scanning capabilities through function calling. This plugin enables LLMs to perform network discovery and security scanning tasks using the powerful Nmap tool.

Head over to our blog for [a full write up](https://hackertarget.com/llm-command-line-nmap/) of the experiment.

## Features

- **Network Discovery**: Get local network information and suggested scan ranges
- **Port Scanning**: Scan specific ports or ranges on target hosts
- **Service Detection**: Identify services and versions running on open ports
- **OS Detection**: Attempt to identify target operating systems
- **Ping Scanning**: Discover live hosts on a network
- **Script Scanning**: Run Nmap NSE scripts for advanced detection
- **Quick Scanning**: Fast scans of common ports

## Prerequisites

- Python 3.7+
- [LLM](https://llm.datasette.io/) - Simon Willison's command-line tool for Large Language Models
- [Nmap](https://nmap.org/) - Network exploration tool and security scanner

### Installation

1. Working LLM tool, ensure the tool and model plugins (llm-gemini) are updated:
```bash
llm models
```

2. Working Nmap Install:
   - **Ubuntu/Debian**: `sudo apt-get install nmap`
   - **macOS**: `brew install nmap`
   - **Windows**: Download from [nmap.org](https://nmap.org/download.html)

3. The llm-tools-nmap.py functions were created as a quick experiment. Simply launch using the --functions capability.
```bash
llm --functions llm-tools-nmap.py "scan my network for open databases"
```


## Available Functions

### Network Information
- `get_local_network_info()`: Discovers local network interfaces, IP addresses, and suggests scan ranges

### Nmap Scanning Functions
- `nmap_scan(target, options="")`: Generic Nmap scan with custom options
- `nmap_quick_scan(target)`: Fast scan of common ports (-T4 -F)
- `nmap_port_scan(target, ports)`: Scan specific ports
- `nmap_service_detection(target, ports="")`: Service version detection (-sV)
- `nmap_os_detection(target)`: Operating system detection (-O)
- `nmap_ping_scan(target)`: Ping scan to discover live hosts (-sn)
- `nmap_script_scan(target, script, ports="")`: Run NSE scripts

## Usage Examples

Once installed, you can use these functions through LLM's function calling capability:

```bash
# Discover your local network
llm --functions llm-tools-nmap.py "What's my local network information?"

# Find live hosts on your network
llm --functions llm-tools-nmap.py "Scan my local network to find live hosts"

# Quick port scan of a hosts in /etc/hosts using pipe capability
cat /etc/hosts | llm --functions llm-tools-nmap.py "Do a quick port scan of these hosts"

# Detailed service detection
llm --functions llm-tools-nmap.py "Scan 192.168.1.1 for services on ports 80,443,22"

```

## Security Considerations

- Beware when giving LLM access to security and command line tools - bad things might happen THIS IS EXPERIMENTAL FUNCTIONALITY
- Some Nmap features (like OS detection) require root/administrator privileges
- Always ensure you have permission to scan target networks
- Be aware of your organization's security policies regarding network scanning

## Related Projects

This plugin is built for use with:
- **[LLM](https://llm.datasette.io/)** by [Simon Willison](https://github.com/simonw) - The foundational tool that enables LLMs to use function calling
- **[Nmap](https://nmap.org/)** - The industry-standard network scanning tool

## License

This project is open source. Please ensure compliance with your local laws and organizational policies when using network scanning tools.


---

