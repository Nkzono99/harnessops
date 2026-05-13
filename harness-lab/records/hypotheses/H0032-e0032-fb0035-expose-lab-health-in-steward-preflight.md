---
id: H0032
record_type: hypothesis
created_at: '2026-05-14T00:58:55+09:00'
status: proposed
target_capability: daily_steward_orchestration
source_eval_case: E0032
---

# H0032: E0032-fb0035-expose-lab-health-in-steward-preflight の仮説

## 仮説

Steward preflight should expose lab health alongside overlay counts so daily runs can route stale lab memory and lab pressure without a separate manual lint step.

## メカニズム

Reuse the existing non-writing lab memory lint result inside steward_preflight for lab repositories, summarize it as lab_health, and make the librarian lane trigger reason name stale memory or pressure when present.

## 最小実装

Add lab_health to steward_preflight JSON/text output for upstream/meta lab repos, leave project repos unchanged, and add focused steward tests for both needs-abstraction and feedback-source behavior.

## 代替案: 削除または統合

Keep preflight count-only and require agents to run hops lab memory lint separately, but that hides a deterministic trigger the steward already needs for daily routing.

## 期待される利点

Daily steward runs can choose the librarian lane based on stale snapshot/semantic memory state rather than vague record counts.

## 想定される欠点

Preflight output becomes slightly larger and could tempt agents to do memory abstraction inside the deterministic preflight instead of delegating to the librarian lane.

## 評価計画

Run tests/test_cli/test_steward.py plus doctor and migrate checks; verify live preflight JSON includes lab_health.status and recommended commands without changing state.

## 中止基準

Reject or narrow if preflight writes files, fails project repositories without harness-lab, or moves judgment-heavy candidate selection into the deterministic preflight.
