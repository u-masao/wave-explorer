# Wave Explorer

このプロジェクトは、Spotify APIを使用して音楽を検索し、再生するためのAIエージェントを提供します。エージェントは、ユーザーのリクエストに基づいて音楽を推薦し、Spotifyでの再生をサポートします。

## 主な機能

- ユーザーのリクエストに基づいて音楽を検索
- Spotify APIを使用して音楽を再生
- エージェントによる音楽の推薦

## 必要な環境変数

### SPOTIFY_CLIENT_ID と SPOTIFY_CLIENT_SECRET の取得方法

1. [Spotify Developer Dashboard](https://developer.spotify.com/) にログインします。アカウントがない場合は作成してください。
2. `Dashboard` で `Create app` をクリックし、必要事項を入力します。
   - `アプリ名`
   - `アプリの説明`
   - `リダイレクトURL`
   - `API / SDK` の同意にチェックを入れ、`保存`をクリックします。
   - `APIs used` には `Web Playback SDK` にチェックを入れてください。
3. 作成したアプリの `Home` の `Settings` から `CLIENT ID` と `CLIENT SECRET` を確認できます。

以下の環境変数を設定する必要があります。`.env`ファイルを使用して設定することができます。

- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIPY_REDIRECT_URI`  
  `SPOTIPY_REDIRECT_URI` は Dashboard で設定する Redirect URI と一致させる必要があります。例えば、`http://127.0.0.1:8888/` などとしてください。  
  **注意: `SPOTIPY_` で始まります。`SPOTIFI_` ではありません。FとPの違いに注意してください。**
- `MCP_SPOTIFY_PATH`

## MCP サーバーのインストール

Wave Explorer を実行する前に、MCP サーバーをインストールする必要があります。以下のコマンドを使用して、MCP サーバーをクローンしてください。

```bash
git clone https://github.com/varunneal/spotify-mcp.git ../spotify-mcp/
```

## 実行方法

1. 必要なPythonパッケージをインストールします。
2. 環境変数を設定します。
3. 以下のコマンドを実行してプログラムを開始します。

```bash
python src/main.py
```

プログラムが開始されると、AIエージェントがユーザーの指示に従って音楽を検索し、再生します。

## 注意事項

- Spotify APIの利用には、Spotifyの開発者アカウントが必要です。
- 環境変数の設定が正しく行われていることを確認してください。
