---
id: FB0026
record_type: imported_feedback
created_at: '2026-05-13T19:13:07+09:00'
status: triaged
source:
  type: local-capture
  original_id:
  source_project: harnessops
classification:
  capability: daily_steward_orchestration
  failure_class: fragmented_improvement_loop
links:
  eval_case:
  issue_url:
---

# FB0026: Add daily steward orchestration skill

## 概要

HarnessOps needs a recurring conductor workflow that can read operational issues, feedback, lab state, doctor/update state, run divergent invention lanes, route candidates, advance eval/hypothesis/guard work, and inspect the improvement loop itself across HarnessOps core, target repositories, and project repositories. External review supported the conductor design but requested explicit write policy, lane triggers, subagent I/O schemas, idempotency, and null-action handling; the Advance lane remains intentionally included for full automation.

## 再現

A daily run over open operational issues currently requires manually choosing between issue triage, open meta scan, research routing, lab advancement, update-harness, and loop-audit skills. Without a conductor, the loop either stays manual or collapses into one over-scaffolded skill.

## 期待する上流変更

Add a packaged hops-daily-steward skill that orchestrates issue triage, open meta scan, librarian, critic, maintainer, evaluator, and advance lanes with explicit run modes, write gates, subagent output schema, no-op policy, and report/ledger sections while delegating state changes to hops CLI.
