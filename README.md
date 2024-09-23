# approved-npo-data

本リポジトリは認定 NPO 法人のデータを取得するためのリポジトリです
devcontainer の設定をしていますので、VS Code と Docker、Git さえあれば各種開発用設定が行われた Python の開発環境が構築され、即時開発が可能です

## 内容

- [devcontainer](https://code.visualstudio.com/docs/remote/containers)
- [Rye](https://rye.astral.sh/)
  - [ruff](https://beta.ruff.rs/docs/)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance), [pyright](https://github.com/microsoft/pyright)
- [hadolint](https://github.com/hadolint/hadolint)
- [pytest](https://docs.pytest.org/en/stable/)
- [GitHub Actions](https://github.co.jp/features/actions)
- [logging](https://docs.python.org/ja/3/howto/logging.html)

## 環境詳細

- Python : 3.12

### 事前準備

- Docker インストール
- VS Code インストール
- VS Code の拡張機能「Remote - Containers」インストール
  - https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
- 本リポジトリの clone
- ssh-agent の設定
  - https://code.visualstudio.com/docs/devcontainers/containers#_using-a-credential-helper

### 開発手順

1. VS Code 起動
2. 左下のアイコンクリック
3. 「Dev Containers: Reopen in Container」クリック
4. しばらく待つ
   - 初回の場合コンテナー image の取得や作成が行われる
5. 起動したら開発可能
   - 初回起動時は `rye sync` を実行してください

## NOTE

- ユニットテスト
  - `rye test`
- lint
  - `rye lint`
- format
  - `rye format`
  - `rye format --check`
