# Wave Explorer

このプロジェクトは、Spotify APIを使用して音楽を検索し、再生するためのAIエージェントを提供します。エージェントは、ユーザーのリクエストに基づいて音楽を推薦し、Spotifyでの再生をサポートします。

## 主な機能

- ユーザーのリクエストに基づいて音楽を検索
- Spotify APIを使用して音楽を再生
- エージェントによる音楽の推薦


## API の準備

### OpenAI API キーの取得方法

1. [OpenAIのウェブサイト](https://www.openai.com/)にアクセスし、アカウントを作成またはログインします。
2. ダッシュボードからAPIキーを取得します。

### SPOTIFY_CLIENT_ID と SPOTIFY_CLIENT_SECRET の取得方法

1. [Spotify Developer Dashboard](https://developer.spotify.com/) にログインします。アカウントがない場合は作成してください。
2. `Dashboard` で `Create app` をクリックし、必要事項を入力します。
   - `アプリ名`
   - `アプリの説明`
   - `リダイレクトURL`
     `https://` が要求されますが、`http://127.0.0.1:8888/` などの URI は入力可能です。  
     spotify-mcp の公式ドキュメントとは設定が異なりますので注意。
   - `APIs used` では `Web Playback SDK` にチェックを入れてください。
   - `API / SDK` の同意にチェックを入れ、`保存`をクリックします。
3. 作成したアプリの `Home` の `Settings` から `CLIENT ID` と `CLIENT SECRET` を確認できます。

## 環境設定

### リポジトリのクローン

以下のコマンドでリポジトリをクローンします

```bash
https://github.com/u-masao/wave-explorer.git
cd wave-explorer
```

### Spotify MCP サーバーの取得

Spotify API を利用するための MCP サーバーを取得します。
以下のコマンドを使用して、MCP サーバーをクローンしてください。

```bash
git clone https://github.com/varunneal/spotify-mcp.git ../spotify-mcp/
```

### 環境変数の設定ファイル

以下の環境変数を設定する必要があります。`.env` ファイルを使用して設定することができます。`.env.example` を参考にしてください。

- `OPENAI_API_KEY`
- `OPENAI_AGENTS_DISABLE_TRACING` OpenAI Platform で Trace したくない場合は 1 にします
- `MCP_SPOTIFY_PATH` MCP Server のパスです( ../spotify-mc/ としています)
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIPY_REDIRECT_URI`
  `SPOTIPY_REDIRECT_URI` は Dashboard で設定する Redirect URI と一致させる必要があります。
  **重要な注意: `SPOTIPY_` で始まります。`SPOTIFI_` ではありません。F と P の違いに注意してください。**

```text:.env.example
OPENAI_API_KEY=your_api_key
OPENAI_AGENTS_DISABLE_TRACING=0
MCP_SPOTIFY_PATH=../spotify-mcp/
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI="http://127.0.0.1:8888/" # Spotify APP の設定と一致させる
```


## 実行方法

1. `uv` コマンドをインストール -> [手順](https://docs.astral.sh/uv/getting-started/installation/)
2. `.env` ファイルを確認
3. 必要な Python パッケージをインストール
4. 以下のコマンドを実行してプログラムを開始

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh # uv のインストール例
cat .env  # .env ファイルの内容を表示
uv sync
uv run python -m src.main
```

プログラムが開始されると、AIエージェントがユーザーの指示に従って音楽を検索し、再生します。

再生開始後はユーザの入力を受け付けるモードに移行します。履歴は記憶させていないので「さっきのアレをアレして」みたいなことはできません。

## 注意事項

- Spotify APIの利用には、Spotifyの開発者アカウントが必要です。
- 環境変数の設定が正しく行われていることを確認してください。
- 極端な使い方をするとレートリミットにかかります。
