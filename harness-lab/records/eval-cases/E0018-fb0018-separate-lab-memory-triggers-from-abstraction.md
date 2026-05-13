---
id: E0018
record_type: eval_case
created_at: '2026-05-13T09:28:04+09:00'
status: active
capability: lab_memory_compaction
failure_class: deterministic_snapshot_conflates_trigger_and_abstraction
source_feedback: FB0018
---

# E0018: FB0018-separate-lab-memory-triggers-from-abstraction を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0018-separate-lab-memory-triggers-from-abstraction.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0018`
- observation: Current lab compaction is a deterministic aggregation snapshot, but the desired dream-like behavior needs lint-style trigger checks and a skill-guided abstraction workflow.

## タスク

`lab_memory_compaction` の `deterministic_snapshot_conflates_trigger_and_abstraction` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

ローカル改善作業中に観測。

## 期待される挙動

Keep source-linked deterministic snapshots as an index, add lint/prepare commands for compaction triggers, and provide an agent skill that performs higher-level lab memory abstraction with source traceability.

## 合格基準

- `deterministic_snapshot_conflates_trigger_and_abstraction` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0018 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `deterministic_snapshot_conflates_trigger_and_abstraction` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
