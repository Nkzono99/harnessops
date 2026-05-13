---
id: IMP0029
record_type: improvement_dossier
created_at: '2026-05-14T00:58:24+09:00'
updated_at: '2026-05-14T01:05:00+09:00'
status: adopted
source_type: friction
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: harnessops-protocol
source_feedback: FB0035
eval_cases:
- E0032
hypotheses:
- H0032
decisions:
- D0033
research_scans:
- RS0005
classification:
  capability: daily_steward_orchestration
  failure_class: count_based_preflight_misses_stale_lab_health
guard:
  status: implemented
  path: tests/test_cli/test_steward.py; tests/test_agent_harness_contract.py
investigation:
- created_at: '2026-05-14T01:04:35+09:00'
  kind: implementation-note
  summary: Implemented lab_health in steward_preflight by reusing the existing non-writing lab memory lint result for upstream/meta lab repos. The JSON now includes status, pressure, triggers, stale snapshot/abstraction state, and recommended commands; the librarian lane reason names needs-abstraction triggers. Feedback-source project repos report lab_health unavailable instead of probing harness-lab memory.
  evidence_ref: src/harnessops/core/steward.py; tests/test_cli/test_steward.py
links:
  issue_url:
---

# IMP0029: FB0035: Expose lab health in steward preflight

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0035`
- linked_records: `FB0035`, `RS0005`, `E0032`, `H0032`, `D0033`

## Source Observation

Source: `harness-lab/records/feedback/FB0035-expose-lab-health-in-steward-preflight.md`

# FB0035: Expose lab health in steward preflight

## 概要

hops steward preflight reports overlay counts and lane triggers, but it does not surface lab memory pressure or stale snapshot/semantic memory state as actionable daily steward input.

## 再現

Run hops steward preflight --json in a meta-lab repository where hops lab memory lint --warn-only reports needs-abstraction; the preflight JSON only shows counts and generic librarian trigger information.

## 期待する上流変更

Steward preflight should include source-linked lab health status and trigger reasons so daily runs can route stale memory or lab pressure to the librarian lane without relying on manual follow-up commands.

## Target Capability

- capability: daily_steward_orchestration
- failure_class: count_based_preflight_misses_stale_lab_health

## Investigation

- 2026-05-14T01:04:35+09:00 [implementation-note] Implemented lab_health in steward_preflight by reusing the existing non-writing lab memory lint result for upstream/meta lab repos. The JSON now includes status, pressure, triggers, stale snapshot/abstraction state, and recommended commands; the librarian lane reason names needs-abstraction triggers. Feedback-source project repos report lab_health unavailable instead of probing harness-lab memory. (evidence: src/harnessops/core/steward.py; tests/test_cli/test_steward.py)

## Research Scans

### RS0005: RS0005: Route lab health through steward preflight


Source: `harness-lab/records/research-scans/RS0005-route-lab-health-through-steward-preflight.md`


# RS0005: Route lab health through steward preflight

## Scope

- scope: harnessops-core daily steward preflight
- existing_dossier: FB0035
- capability: daily_steward_orchestration
- failure_class: count_based_preflight_misses_stale_lab_health

## Evidence

### Local

- Open scan found lab memory lint needs-abstraction while preflight showed only counts and generic lane triggers (ref: harness-lab/records/feedback/FB0035-expose-lab-health-in-steward-preflight.md)

### Codebase

- steward_preflight builds overlay counts and lane triggers but does not call lab memory lint (ref: src/harnessops/core/steward.py)
- lab memory lint already returns status, triggers, recommended commands, stale snapshot, and stale abstraction (ref: src/harnessops/core/lab_memory_lint.py)

### External

- なし

### Risk And Counterexample

- Putting too much analysis into preflight could turn the steward into a workflow engine instead of a deterministic intake command (ref: docs/design-principles.md)

## Candidates

| candidate | relation | recommendation | next_command |
|---|---|---|---|
| Add lab_health to steward preflight and librarian lane trigger reasons | extends | propose | hops lab new-eval-case --from FB0035 |

## Recommendation

propose a narrow deterministic preflight extension: include lab_health only for lab repos, reuse existing lint output, and keep downstream judgment in the librarian lane.

## Next Commands

- `hops lab new-eval-case --from FB0035`


## Evaluation

### E0032: E0032: FB0035-expose-lab-health-in-steward-preflight を評価


- source: `harness-lab/records/eval-cases/E0032-fb0035-expose-lab-health-in-steward-preflight.md`

- capability: daily_steward_orchestration

- failure_class: count_based_preflight_misses_stale_lab_health

- manual_eval_yml: `harness-lab/views/eval-results/E0032-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0032-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=5, regression_risk=2, operator_burden=5, anti_theater=5, maintainability=4, privacy_sanitization_risk=5
- notes: Implemented a narrow deterministic preflight extension. Validation: uv run pytest -q passed 94 tests; uv run ruff check changed files passed; hops doctor --check-overlay --check-records ok; hops migrate --check reported no pending migrations. Live preflight JSON now exposes lab_health.status=needs-abstraction and routes librarian with stale-memory trigger reasons.


## Hypotheses

### H0032: H0032: E0032-fb0035-expose-lab-health-in-steward-preflight の仮説


Source: `harness-lab/records/hypotheses/H0032-e0032-fb0035-expose-lab-health-in-steward-preflight.md`


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


## Evidence

`harness-lab/views/eval-results/E0032-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_steward.py; tests/test_agent_harness_contract.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0033: D0033: adopted H0032


Source: `harness-lab/records/decisions/D0033-adopted-h0032.md`


# D0033: adopted H0032

## 判断

adopted

## 理由

The change keeps steward preflight deterministic while surfacing an existing non-writing lab memory signal that daily runs already need for routing.

## 証拠

Implemented lab_health in steward_preflight; added steward tests for stale lab health and project-repo skip behavior; updated daily steward docs and packaged skills; validation passed: uv run pytest -q, uv run ruff check changed files, hops doctor --check-overlay --check-records, hops migrate --check.

## 回帰リスク

Low to moderate. Preflight JSON grows and now calls lab memory lint for lab repos, but the lint path is read-only and project repos explicitly skip lab health.

## フォローアップ

Consider a later ranking view that orders triggered lanes by lab_health, guard gaps, and stale adopted decisions; keep it out of deterministic preflight until evidence justifies it.

## 回帰ガード

tests/test_cli/test_steward.py; tests/test_agent_harness_contract.py
