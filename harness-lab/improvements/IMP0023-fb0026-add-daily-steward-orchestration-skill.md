---
id: IMP0023
record_type: improvement_dossier
created_at: '2026-05-13T19:15:21+09:00'
updated_at: '2026-05-13T19:45:33+09:00'
status: adopted
source_type: friction
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: harnessops-protocol
source_feedback: FB0026
eval_cases:
- E0026
hypotheses:
- H0026
decisions:
- D0027
research_scans: []
classification:
  capability: daily_steward_orchestration
  failure_class: fragmented_improvement_loop
guard:
  status: implemented
  path: tests/test_agent_harness_contract.py; tests/test_cli/test_steward.py
investigation:
- created_at: '2026-05-13T19:23:30+09:00'
  kind: implementation-note
  summary: 'Codex App automation on an always-on night-run PC should start with a pull-first preflight: inspect branch/remotes, fetch --prune, fast-forward pull on a clean worktree, and stop for human review on dirty/diverged/conflict states before HOPS state changes or Advance. The daily steward skill, docs, and packaging tests now encode that remote-latest assumption.'
  evidence_ref:
- created_at: '2026-05-13T19:28:31+09:00'
  kind: implementation-note
  summary: Daily steward skill now documents that SKILL.md cannot force subagent startup by itself; when the automation prompt explicitly authorizes subagents, the main agent should produce a Subagent Plan, spawn triggered lanes where available, and report inline-fallback reasons when tool/runtime constraints prevent delegation. The open divergent invention lane is named explicitly through open-inventor / Open Meta Scan so daily runs keep the divergent idea source separate from selection and routing.
  evidence_ref:
- created_at: '2026-05-13T19:36:10+09:00'
  kind: implementation-note
  summary: Deterministic daily steward work is now coded as hops steward preflight. The command handles pull-first safety, doctor/check-records, migrate check, overlay counts, lane trigger scaffold, subagent plan scaffold, and run ledger JSON so agents do not spend reasoning on routine intake. The skill now starts automation runs with hops steward preflight --pull --json and only delegates the judgment-heavy lanes to agents/subagents.
  evidence_ref: tests/test_cli/test_steward.py
- created_at: '2026-05-13T19:45:33+09:00'
  kind: implementation-note
  summary: 'Daily steward was compacted into a thin conductor skill: intent, stop gates, delegation, triggers, selection, advance-local, end-of-run policy, decision card, and report only. Routine preflight remains in hops steward preflight; the new hops steward finalize command handles patch-only versus commit-local so unattended advance does not leave the next scheduled run permanently blocked by its own dirty worktree. The wording now treats Advance as human-review-independent local progress, while preserving automated evidence, validation, guard, and privacy gates.'
  evidence_ref: .agents/skills/hops-daily-steward/SKILL.md
links:
  issue_url:
---

# IMP0023: FB0026: Add daily steward orchestration skill

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0026`
- linked_records: `FB0026`, `E0026`, `H0026`, `D0027`

## Source Observation

Source: `harness-lab/records/feedback/FB0026-add-daily-steward-orchestration-skill.md`

# FB0026: Add daily steward orchestration skill

## 概要

HarnessOps needs a recurring conductor workflow that can read operational issues, feedback, lab state, doctor/update state, run divergent invention lanes, route candidates, advance eval/hypothesis/guard work, and inspect the improvement loop itself across HarnessOps core, target repositories, and project repositories. External review supported the conductor design but requested explicit write policy, lane triggers, subagent I/O schemas, idempotency, and null-action handling; the Advance lane remains intentionally included for full automation.

## 再現

A daily run over open operational issues currently requires manually choosing between issue triage, open meta scan, research routing, lab advancement, update-harness, and loop-audit skills. Without a conductor, the loop either stays manual or collapses into one over-scaffolded skill.

## 期待する上流変更

Add a packaged hops-daily-steward skill that orchestrates issue triage, open meta scan, librarian, critic, maintainer, evaluator, and advance lanes with explicit run modes, write gates, subagent output schema, no-op policy, and report/ledger sections while delegating state changes to hops CLI.

## Target Capability

- capability: daily_steward_orchestration
- failure_class: fragmented_improvement_loop

## Investigation

- 2026-05-13T19:23:30+09:00 [implementation-note] Codex App automation on an always-on night-run PC should start with a pull-first preflight: inspect branch/remotes, fetch --prune, fast-forward pull on a clean worktree, and stop for human review on dirty/diverged/conflict states before HOPS state changes or Advance. The daily steward skill, docs, and packaging tests now encode that remote-latest assumption.
- 2026-05-13T19:28:31+09:00 [implementation-note] Daily steward skill now documents that SKILL.md cannot force subagent startup by itself; when the automation prompt explicitly authorizes subagents, the main agent should produce a Subagent Plan, spawn triggered lanes where available, and report inline-fallback reasons when tool/runtime constraints prevent delegation. The open divergent invention lane is named explicitly through open-inventor / Open Meta Scan so daily runs keep the divergent idea source separate from selection and routing.
- 2026-05-13T19:36:10+09:00 [implementation-note] Deterministic daily steward work is now coded as hops steward preflight. The command handles pull-first safety, doctor/check-records, migrate check, overlay counts, lane trigger scaffold, subagent plan scaffold, and run ledger JSON so agents do not spend reasoning on routine intake. The skill now starts automation runs with hops steward preflight --pull --json and only delegates the judgment-heavy lanes to agents/subagents. (evidence: tests/test_cli/test_steward.py)
- 2026-05-13T19:45:33+09:00 [implementation-note] Daily steward was compacted into a thin conductor skill: intent, stop gates, delegation, triggers, selection, advance-local, end-of-run policy, decision card, and report only. Routine preflight remains in hops steward preflight; the new hops steward finalize command handles patch-only versus commit-local so unattended advance does not leave the next scheduled run permanently blocked by its own dirty worktree. The wording now treats Advance as human-review-independent local progress, while preserving automated evidence, validation, guard, and privacy gates. (evidence: .agents/skills/hops-daily-steward/SKILL.md)

## Research Scans

research scan はまだありません。


## Evaluation

### E0026: E0026: FB0026-add-daily-steward-orchestration-skill を評価


- source: `harness-lab/records/eval-cases/E0026-fb0026-add-daily-steward-orchestration-skill.md`

- capability: daily_steward_orchestration

- failure_class: fragmented_improvement_loop

- manual_eval_yml: `harness-lab/views/eval-results/E0026-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0026-manual-score.md`
- scores: impact=5, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=3, operator_burden=3, anti_theater=4, maintainability=4, privacy_sanitization_risk=2
- notes: Implemented hops-daily-steward as a conductor skill rather than a monolithic improver. It includes run modes, write policy, lane trigger matrix, context-separated subagent lanes, structured lane output schema, run ledger reporting, no-op policy, remote confirmation gates, and an Advance lane that can progress eval/implementation/guard/update work when evidence is sufficient. Packaged Codex/Claude copies are synchronized and contract-tested.


## Hypotheses

### H0026: H0026: E0026-fb0026-add-daily-steward-orchestration-skill の仮説


Source: `harness-lab/records/hypotheses/H0026-e0026-fb0026-add-daily-steward-orchestration-skill.md`


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


## Evidence

`harness-lab/views/eval-results/E0026-manual-score.md`

## Guard

- status: implemented
- path: tests/test_agent_harness_contract.py; tests/test_cli/test_steward.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0027: D0027: adopted H0026


Source: `harness-lab/records/decisions/D0027-adopted-h0026.md`


# D0027: adopted H0026

## 判断

adopted

## 理由

The daily steward conductor skill provides the recurring multi-lane improvement entrypoint needed for full automation while preserving HarnessOps state and remote-write safety gates.

## 証拠

Added repo-local and packaged hops-daily-steward skills; updated docs; uv run pytest tests/test_agent_harness_contract.py; uv run ruff check tests/test_agent_harness_contract.py; skill quick_validate passed; manual eval E0026.

## 回帰リスク

Moderate. High-level orchestration can become governance overhead if used on every run without triggers, but no-op, trigger matrix, critic lane, and remote gates reduce the risk.

## フォローアップ

Add a behavioral steward fixture that verifies issue clusters are synthesized instead of proliferating records, and consider a future hops steward command for persistent run ledger/cache.

## 回帰ガード

tests/test_agent_harness_contract.py
