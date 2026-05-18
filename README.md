# HarnessOps

HarnessOps は、AI Agent がハーネスプロジェクトの失敗、フィードバック、評価、改善判断を証拠付きで扱うための運用基盤です。

このプロジェクトは基本的にAI経由で利用します。人間がCLI手順を覚えることより、何をAI Agentに任せるか、どこに記録が残るか、どの安全条件が守られるかを把握することを重視します。

## 人間が把握すること

HarnessOps は3つのリポジトリ役割を分けます。

| レイヤー | オーバーレイ | 目的 |
|---|---|---|
| プロジェクトリポジトリ | `harness-feedback/` | 失敗、ローカル回避策、上流へ送る候補を記録します。 |
| ターゲットリポジトリ | `harness-lab/` | 受け取ったフィードバックを評価ケース、仮説、判断に変換します。 |
| HarnessOps リポジトリ | `harness-lab/` | HarnessOps 自身のCLI、スキーマ、プラグイン、運用ループを改善します。 |

プロジェクト固有の研究方針、論文内容、実験転換は `harness-feedback/` ではなく、各プロジェクトの `research/` または `notes/` に置きます。上流やメタ改善へ回す内容は、必ずルーティングとサニタイズを通します。

普通のリポジトリを汚さず開発時だけ使う場合は、global registry + local state を使えます。

```bash
uvx --from harnessops hops project link --storage local --profile generic-code
uvx --from harnessops hops project resolve --json
uvx --from harnessops hops doctor --check-overlay
uvx --from harnessops hops install-codex-plugin
```

この導線では対象repoに `.harnessops/`、`harness-feedback/`、`harness-lab/` を作らず、`~/.harnessops/projects/<project-id>/` に状態を置きます。共有が必要になった時だけ `hops local pack/import/merge` を使います。詳しくは [docs/global-local-state.md](docs/global-local-state.md) を読んでください。

## 名前

- GitHub repository: `Nkzono99/harnessops`
- PyPI package: `harnessops`
- Python import: `harnessops`
- CLI: `hops`

## 読む順番

- 人間がAI Agent経由で使い始める: [docs/get-started-with-agent.md](docs/get-started-with-agent.md)
- 普通のrepoを汚さず local state で使う: [docs/global-local-state.md](docs/global-local-state.md)
- AI Agent向けの運用手順: [docs/agent-user-guide.md](docs/agent-user-guide.md)
- Codex App automationで日次改善ループを回す: [docs/daily-steward-automation.md](docs/daily-steward-automation.md)
- target repositoryへ組み込むAgentに渡す文書: [docs/target-integration-agent-brief.md](docs/target-integration-agent-brief.md)
- project repository単体へ組み込むAgentに渡す文書: [docs/project-repository-integration-agent-brief.md](docs/project-repository-integration-agent-brief.md)
- 現行仕様の正本: [SPEC.md](SPEC.md)
- 現在のCLI surface: [specs/cli-spec.md](specs/cli-spec.md)
- 設計思想: [docs/design-principles.md](docs/design-principles.md)
- 今後のロードマップ: [docs/roadmap.md](docs/roadmap.md)
- 個別仕様の補助資料: [specs/](specs/)

## 安全上の前提

- `hops` が HarnessOps 状態変更の正本です。Agentやプラグインは、`.harnessops/`、`harness-feedback/`、`harness-lab/` の構造を直接組み替えません。
- Agent向けには repo-local skill と global Codex plugin の2系統があります。どちらも状態変更は `uvx --from harnessops hops ...` に委譲します。global plugin には failure記録、routing、GitHub Issue下書き/作成、local-state pack/import/merge の skill を同梱します。
- 未サニタイズのフィードバックは既定で外部出力されません。
- 採用済み判断には、証拠、回帰リスク、ガードパスが必要です。
- 生成ビューは更新されますが、人が作成した `records/` 配下の履歴はビュー更新で再生成されません。
- `hops` は通常コマンド実行時に `.harnessops/lock.json` と PyPI の version を見て update notice を出します。抑止する場合は `--disable-update-notice`、`HOPS_DISABLE_UPDATE_NOTICE=1`、または PyPI 確認だけ `HOPS_DISABLE_PYPI_UPDATE_CHECK=1` を使います。

## 開発時の確認

```bash
PYTHONPATH="$PWD/src" python3.11 -m pytest -q
uv run --with-editable . hops doctor --check-overlay --check-records
uv run --with-editable . hops migrate --check
```
