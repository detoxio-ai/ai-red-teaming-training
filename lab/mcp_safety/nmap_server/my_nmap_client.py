import argparse
import asyncio
from fastmcp import Client

# Default server URL
DEFAULT_SERVER_URL = "http://127.0.0.1:9000/sse/"

async def main():
    parser = argparse.ArgumentParser(description="MCP Client for running Nmap commands.")
    parser.add_argument("--server", type=str, default=DEFAULT_SERVER_URL, help="MCP server URL (default: 127.0.0.1:9000)")
    parser.add_argument("command", choices=[
        "ping_scan", "quick_scan", "port_scan", "service_detection", "os_detection"
    ], help="Nmap command to run via MCP")
    parser.add_argument("target", type=str, help="Target IP, hostname, or CIDR (e.g. 192.168.1.0/24)")
    parser.add_argument("--ports", type=str, help="Ports to scan (required for port_scan)")

    args = parser.parse_args()

    client = Client(args.server)

    async with client:
        if args.command == "port_scan":
            if not args.ports:
                print("Error: --ports is required for port_scan")
                return
            result = await client.call_tool("port_scan", {"target": args.target, "ports": args.ports})
        else:
            result = await client.call_tool(args.command, {"target": args.target})

        print("\n--- Nmap Output ---\n")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())

