import asyncio
from fastmcp import Client

async def main():
    client = Client("http+uv://127.0.0.1:8000")

    print("🔍 Nmap MCP Client (type 'exit' to quit)")
    while True:
        prompt = input("🧠 Ask: ").strip()
        if prompt.lower() in {"exit", "quit"}:
            break

        try:
            async with client:
                result = await client.call_tool("natural_language_query", {"prompt": prompt})
                print(f"\n📄 Result:\n{result}\n")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

