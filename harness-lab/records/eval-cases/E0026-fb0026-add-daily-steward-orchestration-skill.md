---
id: E0026
record_type: eval_case
created_at: '2026-05-13T19:14:42+09:00'
status: active
capability: daily_steward_orchestration
failure_class: fragmented_improvement_loop
source_feedback: FB0026
---

# E0026: FB0026-add-daily-steward-orchestration-skill を評価

## フィクスチャ

- source_feedback: `harness-lab/records/feedback/FB0026-add-daily-steward-orchestration-skill.md`
- fixture_dir: `harness-lab/records/eval-cases/fixtures/E0026`
- observation: HarnessOps needs a recurring conductor workflow that can read operational issues, feedback, lab state, doctor/update state, run divergent invention lanes, route candidates, advance eval/hypothesis/guard work, and inspect the improvement loop itself across HarnessOps core, target repositories, and project repositories. External review supported the conductor design but requested explicit write policy, lane triggers, subagent I/O schemas, idempotency, and null-action handling; the Advance lane remains intentionally included for full automation.

## タスク

`daily_steward_orchestration` の `fragmented_improvement_loop` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

A daily run over open operational issues currently requires manually choosing between issue triage, open meta scan, research routing, lab advancement, update-harness, and loop-audit skills. Without a conductor, the loop either stays manual or collapses into one over-scaffolded skill.

## 期待される挙動

Add a packaged hops-daily-steward skill that orchestrates issue triage, open meta scan, librarian, critic, maintainer, evaluator, and advance lanes with explicit run modes, write gates, subagent output schema, no-op policy, and report/ledger sections while delegating state changes to hops CLI.

## 合格基準

- `fragmented_improvement_loop` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops eval --case E0026 --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `fragmented_improvement_loop` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
