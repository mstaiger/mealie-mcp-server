# list_mealie_tools.py
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    params = StdioServerParameters(
        command="uv",
        args=[
            "--directory", "/path/to/mealie-mcp-server/src",
            "run", "server.py",
        ],
        env={
            **os.environ,  # keep PATH etc. so uv is found
            "MEALIE_BASE_URL": os.environ["MEALIE_BASE_URL"],
            "MEALIE_API_KEY": os.environ["MEALIE_API_KEY"],
        },
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.list_tools()
            for t in result.tools:
                desc = (t.description or "").strip().splitlines()[0]
                print(f"{t.name:40s}  {desc}")


if __name__ == "__main__":
    asyncio.run(main())
