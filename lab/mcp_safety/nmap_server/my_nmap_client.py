import asyncio
from fastmcp import Client

client = Client("http+uv://127.0.0.1:18801")

async def test():
    async with client:
        result = await client.call_tool("nmap_quick_scan", {"target": "scanme.nmap.org"})
        print(result)

asyncio.run(test())

