# client.py

import asyncio
from fastmcp import Client

client = Client("http+uv://127.0.0.1:18800")

async def run():
    async with client:
        result = await client.call_tool("nmap_scan", {"ip": "192.168.1.1"})
        print(result)

asyncio.run(run())

