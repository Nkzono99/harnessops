---
id: E0037
record_type: eval_case
created_at: '2026-05-17T04:17:49+09:00'
status: active
capability: cli_ergonomics
failure_class: command_surface_sprawl
source_feedback: FB0047
---

# E0037: FB0047-cli-surface-needs-canonical-grouped-commands を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0047-cli-surface-needs-canonical-grouped-commands.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0037`
- observation: HarnessOps CLI now exposes several lifecycle actions as top-level or parallel lab commands, making the recommended path harder to learn and increasing automation ambiguity.

## タスク

`cli_ergonomics` の `command_surface_sprawl` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

ローカル改善作業中に観測。

## 期待される挙動

Group feedback actions under feedback, lab evaluation actions under lab, review actions under lab review, memory compaction under lab memory, and emit deprecation warnings from old entrypoints.

## 合格基準

- `command_surface_sprawl` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops lab eval --case E0037 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `command_surface_sprawl` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
