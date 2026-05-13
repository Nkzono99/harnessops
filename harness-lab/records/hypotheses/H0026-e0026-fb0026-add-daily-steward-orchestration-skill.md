---
id: H0026
record_type: hypothesis
created_at: '2026-05-13T19:14:53+09:00'
status: proposed
target_capability: daily_steward_orchestration
source_eval_case: E0026
---

# H0026: E0026-fb0026-add-daily-steward-orchestration-skill の仮説

## 仮説

A daily steward conductor skill can make HarnessOps' recurring improvement loop usable across core, target, and project repositories by separating issue triage, open invention, memory lookup, critique, selection, maintainer checks, and Advance lanes while delegating state changes to hops.

## メカニズム

The skill gives agents a stable daily entrypoint with explicit run modes, lane triggers, subagent output schema, idempotent run ledger reporting, no-op policy, remote write gates, and an Advance lane that can progress eval, implementation, guard, and update work when evidence is sufficient.

## 最小実装

Add repo-local and packaged hops-daily-steward skills, document daily steward orchestration, and add contract tests that assert packaging, run policy, lane schema, no-op, and remote confirmation guards.

## 代替案: 削除または統合

Keep using separate skills manually, but that leaves the recurring loop fragmented and makes full automation dependent on operator memory. Make daily steward report-only, but that blocks the Advance lane needed for complete loop automation.

## 期待される利点

Daily runs can process operational issues, discover systemic ideas, connect them to memory, critique noise, advance guarded work, and avoid repeated raw-idea rediscovery without collapsing every observation into a new record.

## 想定される欠点

Another high-level skill can become a governance layer if lane triggers and no-op policy are ignored; subagent orchestration may add cost.

## 評価計画

Run focused and full agent harness contract tests, validate the new skill, run ruff, doctor, migrate, and confirm packaged Codex/Claude skill copies match repo-local skills.

## 中止基準

Reject or split the skill if it performs remote writes without confirmation, records Raw Ideas directly, creates lab records in project repos, or loses the Advance lane's evidence/guard requirements.
