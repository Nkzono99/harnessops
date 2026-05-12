# HarnessOps Codex Plugin

このプラグインは、Codex から HarnessOps を扱うための薄いスキル集です。状態変更は必ず `hops` CLI に委譲し、`.harnessops/`、`harness-feedback/`、`harness-lab/` の構造を直接組み替えません。

## Install

HarnessOps リポジトリからユーザー領域へインストールします。

```bash
uv run --with-editable . hops agent install --codex --scope user
```

対象リポジトリだけに最小限の案内を置きたい場合は、repo-local bridge を使います。

```bash
hops agent bridge --codex
```

複数リポジトリで使う場合はユーザー領域のプラグイン、単一リポジトリへ明示的な注意書きを残す場合は repo-local bridge を選びます。

## Contract

- 先に `hops doctor --check-overlay` を実行します。
- 未リンクなら `hops detect` を実行し、検出結果に基づく `hops init --profile <id>` を提案または実行します。
- レコード作成、ルーティング、エクスポート/インポート、ラボ評価、採用判断は `hops` に委譲します。
- 外部共有前に `hops feedback export --sanitize` を使い、ローカルパス、非公開語、未公開研究の文脈を残しません。
- リモートIssue、PR、pushはユーザー確認なしに行いません。
- target固有の triage skill は domain diagnosis だけを担当し、record schema、routing、sanitize、export/import は HarnessOps に委譲します。
- GitHub release は `hops-release` skill の検証、push、`gh release create` 手順に従います。
