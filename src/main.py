import asyncio
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio

load_dotenv()


async def run_agent(
    history: Dict[str, Any], message: str, mcp_servers: List[MCPServer]
):
    # エージェントを定義
    agent = Agent(
        name="アシスタント",
        instructions="ユーザーの指示にしたがって Spotify を操作して",
        mcp_servers=mcp_servers,
    )
    history.append({"role": "user", "content": message})
    result = await Runner.run(starting_agent=agent, input=history)
    print(f"[応答] {result.final_output}")
    return result.to_input_list()


async def run(spotify_mcp: MCPServer):
    """エージェントの定義と実行"""

    query_artist = "竹内まりや"
    count = 3

    history = []
    commands = [
        (f"{query_artist}の代表曲を{count}曲教えて。テーマは失恋です。", False),
        (f"Spotify で artist:{query_artist} の先ほどの{count}曲を検索して", True),
        (f"{count}曲をキューに設定してアクティブなデバイスで再生して", True),
    ]
    for message, use_mcp in commands:
        print(f"[実行中] {message}")
        mcp_servers = [spotify_mcp] if use_mcp else []
        history = await run_agent(history, message, mcp_servers)
        print(f"[応答の詳細]: {history[-1]}")


async def main():
    """メイン処理"""
    params = {
        "command": "uv",
        "args": [
            "--directory",
            os.getenv("MCP_SPOTIFY_PATH"),
            "run",
            "spotify-mcp",
        ],
        "env": {
            "SPOTIFY_CLIENT_ID": os.getenv("SPOTIFY_CLIENT_ID"),
            "SPOTIFY_CLIENT_SECRET": os.getenv("SPOTIFY_CLIENT_SECRET"),
            "SPOTIPY_REDIRECT_URI": os.getenv("SPOTIPY_REDIRECT_URI"),
        },
    }
    async with MCPServerStdio(name="mcp spotify", params=params) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="mcp spotify", trace_id=trace_id):
            print(
                "トレース情報: https://platform.openai.com/traces/trace"
                f"?trace_id={trace_id}\n"
            )
            await run(server)


if __name__ == "__main__":
    asyncio.run(main())
