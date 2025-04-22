import asyncio
import sys
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

import random
from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio
import textwrap

load_dotenv()

DEFAULT_INSTRUCTION = """
    あなたは出版された音楽に関するエキスパートです。
    ユーザーのリクエストにシンプルな回答を与えて。
    必要に応じて Spotify API を操作して。
    SpotifySearch は文字列一致の傾向が強いです。
    そのため、クエリ文字列を短くして一覧を取得し、
    LLMが最適なものを選んで。
"""


async def run_agent(
    history: Dict[str, Any],
    message: str,
    mcp_servers: List[MCPServer],
    model_name: str = "o4-mini",
):
    # エージェントを定義
    agent = Agent(
        name="再生音楽のエキスパート",
        instructions=textwrap.dedent(DEFAULT_INSTRUCTION),
        mcp_servers=mcp_servers,
        model=model_name,
    )

    # メッセージを作成
    history.append({"role": "user", "content": message})

    # エージェントを実行
    result = await Runner.run(starting_agent=agent, input=history)

    # 結果を処理
    print(f"[応答] {result.final_output}")
    return result.to_input_list()


async def run(spotify_mcp: MCPServer, recommend_tracks: int = 3):
    """エージェントの定義と実行"""

    query_artist, track_theme = random.choice(
        [
            ("竹内まりや", "切ない失恋"),
            ("Jeff Beck", "ノリノリのライブトラック"),
            ("The brecker brothers", "ゴリゴリのソロが聞ける曲"),
        ]
    )

    history = []
    commands = [
        (
            f"「{query_artist}」の曲を{recommend_tracks}曲おしえて。"
            f"テーマは「{track_theme}」です。",
            False,
            0,
        ),
        (
            f"Spotify で新しいセッションを作り artist:{query_artist} の"
            f"先ほどの{recommend_tracks}曲を再生して",
            True,
            0,
        ),
    ]
    for message, use_mcp, wait in commands:
        print(f"[実行中] {message}")
        mcp_servers = [spotify_mcp] if use_mcp else []
        history = await run_agent(history, message, mcp_servers)
        print(f"[応答の詳細]: {history[-1]}")
        await asyncio.sleep(wait)

    print("ここからはあなたのターンです。AIエージェントに指示をだし続けて下さい")
    while True:
        try:
            message = input("何します？> ")
        except EOFError:
            print("\n終了します。またね。")
            sys.exit(0)
        if message:
            await run_agent([], message, [spotify_mcp])


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
    async with MCPServerStdio(name="spotify mcp server", params=params) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="wave explorer", trace_id=trace_id):
            print(
                "トレース情報: https://platform.openai.com/traces/trace"
                f"?trace_id={trace_id}\n"
            )
            await run(server)


if __name__ == "__main__":
    asyncio.run(main())
