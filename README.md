# HarnessOps

HarnessOps は、AI支援ハーネスプロジェクトのためのフィードバックルーティングと改善実験のOSです。

自己改善ループを証拠に基づいたまま運用するために使います。AIは変更候補を生成できますが、HarnessOps は失敗を記録し、フィードバックを振り分け、評価ケースを作成し、仮説を残し、スコアカードを保存し、採用または却下の判断を記録します。

## 基本モデル

HarnessOps は3つのリポジトリ役割を分離します。

| レイヤー | オーバーレイ | 責務 |
|---|---|---|
| プロジェクトリポジトリ | `harness-feedback/` | 失敗を観測し、ローカル回避策を記録し、サニタイズ済みフィードバックをエクスポートします。 |
| ターゲットリポジトリ | `harness-lab/` | フィードバックをインポートし、評価ケースを作成し、仮説を評価し、判断を記録します。 |
| HarnessOps リポジトリ | `harness-lab/` | スキーマ、CLI、マイグレーション、プロファイル、アダプタ、プラグインワークフローを改善します。 |

プロジェクト固有の発展は `harness-feedback/` ではなく `research/` または `notes/` に置きます。ターゲットまたはメタ改善として昇格する内容は、必ずルーティングとサニタイズを通します。

## 最小ループ

```bash
hops init --profile runops-project
hops add-failure --title "ハーネス摩擦" --target runops
hops route --record F0001
hops feedback export --sanitize
```

ターゲット側では次のように扱います。

```bash
hops init --profile runops-upstream
hops feedback import path/to/UF0001-runops-feedback.md
hops lab new-eval-case --from FB0001
hops propose --from E0001
hops eval --case E0001 --manual --score impact=4 --score anti-theater=5
hops decide --from H0001 --status parked
```

採用済み判断には、証拠、回帰リスク、ガードパスが必要です。

```bash
hops decide --from H0001 --status adopted \
  --reason "より小さいプロファイル変更で評価が通った" \
  --evidence "harness-lab/views/eval-results/E0001-manual-score.yml" \
  --regression-risk "低い。フィクスチャが失敗クラスを覆っている" \
  --guard-path "tests/test_cli/test_mvp_flow.py"
```

## プライバシー

プロジェクト側の可視性は既定で `private-until-sanitized` です。`hops feedback export` は、`--allow-private` が明示されない限り、未サニタイズ出力を拒否します。サニタイズでは、外部向けフィードバックを書き出す前に、ローカルパス、設定された非公開語、保護パス、送信元プロジェクト識別情報を伏せます。

任意のプロジェクト設定:

```yaml
# .harnessops/sanitize.yml
redact_patterns:
  - pattern: "/home/[^\\s]+"
    replacement: "<LOCAL_PATH>"
private_terms:
  - secret-method-name
```

## エージェントプラグイン

Codex と Claude のプラグインパッケージは `plugins/` にあります。これらは薄いワークフローラッパーです。状態変更には必ず `hops` を呼び出し、`.harnessops/`、`harness-feedback/`、`harness-lab/` の構造を直接組み替えてはいけません。

リポジトリブリッジ:

```bash
hops agent bridge --codex
```

ユーザー領域へのプラグインインストール:

```bash
hops agent install --codex --scope user
```

## 開発

```bash
PYTHONPATH="$PWD/src" python3.11 -m pytest -q
uvx --from . harnessops --help
uv run --with-editable . hops doctor --check-overlay --check-records
```

現在のMVPカバレッジは、検出、初期化、doctor、マイグレーション確認、失敗作成、ルーティング、フィードバックのエクスポート/インポート、評価ケース作成、仮説/判断レコード、スコアカード出力、サニタイズ、上書き安全性を検証します。
