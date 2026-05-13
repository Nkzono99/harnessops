# HarnessOps Codex Plugin

このプラグインは、Codex から HarnessOps を扱うための薄いスキル集です。状態変更は必ず `hops` CLI に委譲し、`.harnessops/`、`harness-feedback/`、`harness-lab/` の構造を直接組み替えません。

## Recommended: repo-local skills

通常の target/project repository では、プラグインではなく repo-local skill 展開を使います。

```bash
hops init --profile <profile-id> --with-agent-bridge
```

すでに初期化済みなら:

```bash
hops agent bridge --codex
```

`hops-add-failure`、`hops-issue-triage`、`hops-compact-lab-memory` などが `.agents/skills/` に展開されます。

## Optional: user plugin

複数リポジトリで同じ global plugin を共有したい場合だけ、HarnessOps リポジトリからユーザー領域へインストールします。

```bash
uv run --with-editable . hops agent install --codex --scope user
codex plugin marketplace add "$HOME"
```

Codex の plugin は marketplace 登録だけでは使えず、Codex の plugin 画面または app-server の `plugin/install` でインストールが必要です。

## Contract

- 先に `hops doctor --check-overlay` を実行します。
- 未リンクなら `hops detect` を実行し、検出結果に基づく `hops init --profile <id>` を提案または実行します。
- レコード作成、ルーティング、エクスポート/インポート、ラボ評価、採用判断は `hops` に委譲します。
- 外部共有前に `hops feedback export --sanitize` を使い、ローカルパス、非公開語、未公開研究の文脈を残しません。
- リモートIssue、PR、pushはユーザー確認なしに行いません。
- target固有の triage skill は domain diagnosis だけを担当し、record schema、routing、sanitize、export/import は HarnessOps に委譲します。
- GitHub issue は `hops-issue-triage` で imported feedback、eval case、hypothesis へ進めます。
- lab memory の抽象化は `hops lab memory lint` と `hops-compact-lab-memory` で扱います。
