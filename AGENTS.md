# HarnessOps エージェントメモ

このリポジトリは HarnessOps 自身の実装リポジトリです。状態変更の正本は `hops` CLI、仕様の正本は `SPEC.md` です。

## 操作ルール

- HarnessOps の状態変更には必ず `hops` を使います。PATH にない場合は `uv run --with-editable . hops <command>` を使います。
- 作業開始時に `.harnessops/project.toml` を読み、必要に応じて `hops doctor --check-overlay --check-records` でリンク状態を確認します。
- HarnessOps 自身の非自明な改善、issue化前の観測、またはrelease対象の挙動変更は、実装前または遅くともrelease前に `hops lab capture` で `harness-lab` に記録します。
- HarnessOps 実装コード自体を編集する場合を除き、`.harnessops/`、`harness-feedback/`、`harness-lab/` の構造を直接組み替えないでください。
- レコード作成、ルーティング、フィードバックのエクスポート/インポート、ラボ評価、採用判断は CLI に委譲します。
- プロジェクト固有の研究方針、論文内容、実験転換は `harness-feedback/` や `harness-lab/` に混ぜず、対象プロジェクトの `research/` または `notes/` に置きます。
- 外部共有前に `hops feedback export --sanitize` を使い、ローカルパス、非公開語、未公開研究の文脈を残さないでください。

## 開発時の確認

- `uv run --with-editable . hops doctor --check-overlay --check-records`
- `uv run --with-editable . hops migrate --check`
- CLI、ブリッジ、プラグインを変えた場合は関連する `pytest` を実行します。
