import asyncio
from fastmcp import Client

SERVER_URL = "http://127.0.0.1:9000/sse/"  # Or replace with your actual server

client = Client(SERVER_URL)

async def main():
    async with client:
        print("🔌 Connected to MCP server.")
        print("💬 Type a natural language query (or 'exit' to quit):\n")

        while True:
            user_input = input("🧠 > ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("👋 Exiting...")
                break

            try:
                response = await client.call_tool("natural_language_query", {"prompt": user_input})
                print("📡 Response:\n", response)
            except Exception as e:
                print(f"❌ Error calling tool: {e}")

if __name__ == "__main__":
    asyncio.run(main())
