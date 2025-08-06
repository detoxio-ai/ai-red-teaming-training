import asyncio
from fastmcp import Client

# Replace this with your actual server URL if different
SERVER_URL = "http://127.0.0.1:9000/sse/"

client = Client(SERVER_URL)

async def greet_user(name: str):
    async with client:
        response = await client.call_tool("greet", {"name": name})
        print("Response:", response)

if __name__ == "__main__":
    asyncio.run(greet_user("UV Client"))


