---
id: E0032
record_type: eval_case
created_at: '2026-05-14T00:58:39+09:00'
status: active
capability: daily_steward_orchestration
failure_class: count_based_preflight_misses_stale_lab_health
source_feedback: FB0035
---

# E0032: FB0035-expose-lab-health-in-steward-preflight を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0035-expose-lab-health-in-steward-preflight.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0032`
- observation: hops steward preflight reports overlay counts and lane triggers, but it does not surface lab memory pressure or stale snapshot/semantic memory state as actionable daily steward input.

## タスク

`daily_steward_orchestration` の `count_based_preflight_misses_stale_lab_health` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

Run hops steward preflight --json in a meta-lab repository where hops lab memory lint --warn-only reports needs-abstraction; the preflight JSON only shows counts and generic librarian trigger information.

## 期待される挙動

Steward preflight should include source-linked lab health status and trigger reasons so daily runs can route stale memory or lab pressure to the librarian lane without relying on manual follow-up commands.

## 合格基準

- `count_based_preflight_misses_stale_lab_health` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0032 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `count_based_preflight_misses_stale_lab_health` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
