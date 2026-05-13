# HarnessOps Claude メモ

このリポジトリは HarnessOps 自身の実装リポジトリです。管理対象状態の変更は `hops` CLI に委譲し、リポジトリローカルのブリッジスキルと同梱プラグインは薄い案内に限定します。

## 操作ルール

- PATH に `hops` がない場合は `uvx --from harnessops hops <command>` を使います。
- 作業開始時に `.harnessops/project.toml` を読み、必要に応じて `hops doctor --check-overlay --check-records` を実行します。
- HarnessOps 自身の非自明な改善、issue化前の観測、またはrelease対象の挙動変更は、実装前または遅くともrelease前に `hops lab capture` で `harness-lab` に記録します。
- HarnessOps 実装コード自体を編集する場合を除き、`.harnessops/`、`harness-feedback/`、`harness-lab/` の構造を直接組み替えないでください。
- レコード作成、ルーティング、フィードバックのエクスポート/インポート、ラボ評価、採用判断は CLI に委譲します。
- 外部共有前に `hops feedback export --sanitize` を使い、ローカルパス、非公開語、未公開研究の文脈を残さないでください。

## 開発時の確認

- `uv run --with-editable . hops doctor --check-overlay --check-records`
- `uv run --with-editable . hops migrate --check`
