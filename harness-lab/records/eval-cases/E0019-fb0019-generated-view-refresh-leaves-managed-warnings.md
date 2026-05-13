---
id: E0019
record_type: eval_case
created_at: '2026-05-13T11:44:58+09:00'
status: active
capability: generated_view_management
failure_class: stale_generated_view_repair_gap
source_feedback: FB0019
---

# E0019: FB0019-generated-view-refresh-leaves-managed-warnings を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0019-generated-view-refresh-leaves-managed-warnings.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0019`
- observation: The current lab refresh-views command refreshes dynamic lab views but leaves some doctor-managed generated artifacts stale, so doctor remains ok with generated-view warnings after the apparent repair command.

## タスク

`generated_view_management` の `stale_generated_view_repair_gap` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

Run hops doctor --check-overlay --check-records, then hops lab refresh-views, then doctor again; README, backlog, and score-trajectory warnings remain.

## 期待される挙動

Provide a refresh path that updates every doctor-managed lab generated artifact or clearly reports the next repair action, so operators do not learn to ignore stale generated-view warnings.

## 合格基準

- `stale_generated_view_repair_gap` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0019 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `stale_generated_view_repair_gap` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
