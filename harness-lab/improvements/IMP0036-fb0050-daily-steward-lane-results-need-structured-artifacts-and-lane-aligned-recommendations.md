---
id: IMP0036
record_type: improvement_dossier
created_at: '2026-05-18T03:18:35+09:00'
updated_at: '2026-05-22T03:32:34+09:00'
status: adopted
source_type: observation
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: target-lab-case
source_feedback: FB0050
eval_cases:
- E0040
hypotheses:
- H0040
decisions:
- D0041
research_scans:
- RS0006
classification:
  capability: daily_steward_supervision
  failure_class: implicit_lane_contract
guard:
  status: implemented
  path: tests/test_cli/test_steward.py
investigation:
- created_at: '2026-05-18T03:19:08+09:00'
  kind: codebase
  summary: Steward preflight already exposes supervisor_plan.lane_result_optional_fields.artifacts and lane_artifact_contracts.open-meta-scan with artifacts.meta_scan keys; open-meta handoff names the structured fields; subagent_plan.spawn_recommendations now emits actual supervisor lane names while retaining signal details separately under signals.
  evidence_ref:
- created_at: '2026-05-20T03:23:05+09:00'
  kind: codebase
  summary: Run 20260520-030313 consumed structured open-meta artifacts successfully, but the queue still ranks IMP0001-IMP0005 as five separate adopted-without-implemented-guard items and RS0006 still advertises a dossier command that IMP0036 already satisfies. Treat the remaining pressure as priority-lane queue grouping and stale research-scan retirement, not another lane artifact contract change.
  evidence_ref: .harnessops/cache/steward-runs/20260520-030313-fdb26c1.json; uv run --with-editable . hops lab review queue --json; harness-lab/improvements/IMP0036-fb0050-daily-steward-lane-results-need-structured-artifacts-and-lane-aligned-recommendations.md
- created_at: '2026-05-22T03:32:33+09:00'
  kind: codebase
  summary: 'Run 20260522-030226 consumed structured open-meta artifacts successfully, but issue #40 closure intent and later PR/issue actions still arrive as prose in lane summaries. Keep the existing open-meta artifact contract intact; route any typed finalize-facing intent as a separate FB0044/ledger extension instead of broadening open-meta schema.'
  evidence_ref: supervisor lane summaries for run 20260522-030226-2b11cc3; harness-lab/records/feedback/FB0044-steward-run-ledger-and-lane-result-validation.md; src/harnessops/core/steward.py::validate_lane_result
links:
  issue_url:
---

# IMP0036: FB0050: Daily steward lane results need structured artifacts and lane-aligned recommendations

## Status

- status: adopted
- maturity: adopted
- source_type: observation
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0050`
- linked_records: `FB0050`, `RS0006`, `E0040`, `H0040`, `D0041`

## Source Observation

Source: `harness-lab/records/feedback/FB0050-daily-steward-lane-results-need-structured-artifacts-and-lane-aligned-recommendations.md`

# FB0050: Daily steward lane results need structured artifacts and lane-aligned recommendations

## 概要

Code review found that open-meta-scan results were only described by handoff prose, while subagent spawn recommendations used signal names that did not always match supervisor lane names. This can make downstream invention/priority agents depend on implicit formatting or nonexistent lane identifiers.

## 再現

Review merged PR #30 and inspect src/harnessops/core/steward.py plus daily steward preflight JSON.

## 期待する上流変更

Steward run preflight should expose optional structured lane artifacts for open-meta-scan raw ideas/counterframes/routing hints, and subagent spawn recommendations should align with actual supervisor lanes while keeping signal detail available separately.

## Target Capability

- capability: daily_steward_supervision
- failure_class: implicit_lane_contract

## Investigation

- 2026-05-18T03:19:08+09:00 [codebase] Steward preflight already exposes supervisor_plan.lane_result_optional_fields.artifacts and lane_artifact_contracts.open-meta-scan with artifacts.meta_scan keys; open-meta handoff names the structured fields; subagent_plan.spawn_recommendations now emits actual supervisor lane names while retaining signal details separately under signals.
- 2026-05-20T03:23:05+09:00 [codebase] Run 20260520-030313 consumed structured open-meta artifacts successfully, but the queue still ranks IMP0001-IMP0005 as five separate adopted-without-implemented-guard items and RS0006 still advertises a dossier command that IMP0036 already satisfies. Treat the remaining pressure as priority-lane queue grouping and stale research-scan retirement, not another lane artifact contract change. (evidence: .harnessops/cache/steward-runs/20260520-030313-fdb26c1.json; uv run --with-editable . hops lab review queue --json; harness-lab/improvements/IMP0036-fb0050-daily-steward-lane-results-need-structured-artifacts-and-lane-aligned-recommendations.md)
- 2026-05-22T03:32:33+09:00 [codebase] Run 20260522-030226 consumed structured open-meta artifacts successfully, but issue #40 closure intent and later PR/issue actions still arrive as prose in lane summaries. Keep the existing open-meta artifact contract intact; route any typed finalize-facing intent as a separate FB0044/ledger extension instead of broadening open-meta schema. (evidence: supervisor lane summaries for run 20260522-030226-2b11cc3; harness-lab/records/feedback/FB0044-steward-run-ledger-and-lane-result-validation.md; src/harnessops/core/steward.py::validate_lane_result)

## Research Scans

### RS0006: RS0006: Consolidation-first routing for daily steward candidates


Source: `harness-lab/records/research-scans/RS0006-consolidation-first-routing-for-daily-steward-candidates.md`


# RS0006: Consolidation-first routing for daily steward candidates

## Scope

- scope: harnessops-core daily steward invention and priority lanes
- existing_dossier: FB0050
- capability: daily_steward_supervision
- failure_class: autonomous_record_growth_without_selection_pressure

## Evidence

### Local

- Open-meta scan for run 20260518-030245-7e9269e warned that the daily steward can reward producing records faster than retiring, merging, rejecting, or testing them (ref: automation lane handoff)
- Current queue has 25 items and lab health still reports needs-abstraction from file_count>256 after maintenance compaction (ref: hops lab review queue --json; supervisor preflight)

### Codebase

- hops-research-improvements already requires horizon/generalization and park/reject routing before new captures (ref: .agents/skills/hops-research-improvements/SKILL.md)
- FB0050 captures implicit lane contract risk; FB0045 captures missing source-preserving forgetting policy (ref: harness-lab/records/feedback/FB0050-daily-steward-lane-results-need-structured-artifacts-and-lane-aligned-recommendations.md; harness-lab/records/feedback/FB0045-harness-lab-needs-forgetting-policy.md)

### External

- なし

### Risk And Counterexample

- Over-correcting could make invention suppress useful raw discoveries; keep open-meta noisy and enforce consolidation only in downstream routing (ref: open-meta counterframe)

## Candidates

| candidate | relation | recommendation | next_command |
|---|---|---|---|
| Add consolidation-first queue policy to invention/priority lanes | extends | propose after FB0050 dossier exists | hops lab dossier --from FB0050 |
| Design source-preserving archive/exclude policy for stale local-only lab material | extends | queue behind lane contract work | hops lab dossier --from FB0045 |

## Recommendation

Queue a bounded consolidation-first policy through existing FB0050/FB0045 records; priority lane should prefer FB0050 dossier/eval before any new capture.

## Next Commands

- `hops lab dossier --from FB0050`
- `hops lab dossier --from FB0045`


## Evaluation

### E0040: E0040: FB0050-daily-steward-lane-results-need-structured-artifacts-and-lane-aligned-recommendations を評価


- source: `harness-lab/records/eval-cases/E0040-fb0050-daily-steward-lane-results-need-structured-artifacts-and-lane-aligned-recommendations.md`

- capability: daily_steward_supervision

- failure_class: implicit_lane_contract

- manual_eval_yml: `harness-lab/views/eval-results/E0040-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0040-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=4, regression_risk=4, operator_burden=4, anti_theater=5, maintainability=4, privacy_sanitization_risk=5
- notes: H0040 is supported by existing steward contract tests: tests/test_cli/test_steward.py asserts lane_artifact_contracts.open-meta-scan.path, handoff references artifacts.meta_scan and Raw Ideas, spawn recommendation lanes equal supervisor plan lanes, and open-meta lane-result validation rejects missing artifacts.meta_scan.


## Hypotheses

### H0040: H0040: E0040-fb0050-daily-steward-lane-results-need-structured-artifacts-and-lane-aligned-recommendations の仮説


Source: `harness-lab/records/hypotheses/H0040-e0040-fb0050-daily-steward-lane-results-need-structured-artifacts-and-lane-aligned-recommendations.md`


# H0040: E0040-fb0050-daily-steward-lane-results-need-structured-artifacts-and-lane-aligned-recommendations の仮説

## 仮説

Daily steward preflight should make lane handoff contracts machine-checkable enough that downstream lanes do not infer open-meta output shape or nonexistent lane names from prose.

## メカニズム

Expose artifacts as an optional lane result field, define an open-meta-scan artifact contract, require open-meta handoff to return artifacts.meta_scan, and make spawn recommendations use supervisor lane names with triggering signals kept as separate data.

## 最小実装

Keep steward supervisor lanes fixed; add/retain artifacts.meta_scan contract validation for open-meta results and tests that recommendation lanes equal supervisor lanes.

## 代替案: 削除または統合

Continue relying on handoff prose and human-readable signal labels.

## 期待される利点

Later invention and priority lanes can consume structured open-meta output and route work without depending on implicit wording.

## 想定される欠点

The open-meta lane carries a slightly stricter result contract that must be maintained when its schema changes.

## 評価計画

Run steward preflight and lane-result validation tests that assert artifact contract exposure, open-meta handoff text, lane-aligned spawn recommendations, and validation failure when artifacts.meta_scan is missing.

## 中止基準

Reject if validation cannot distinguish lane names from trigger signals or if open-meta lanes can complete without structured artifacts.


## Evidence

`harness-lab/views/eval-results/E0040-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_steward.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0041: D0041: adopted H0040


Source: `harness-lab/records/decisions/D0041-adopted-h0040.md`


# D0041: adopted H0040

## 判断

adopted

## 理由

The steward contract now exposes structured open-meta artifacts and lane-aligned spawn recommendations, reducing implicit downstream lane assumptions.

## 証拠

E0040 manual scorecard plus tests/test_cli/test_steward.py cover preflight artifact contract exposure, handoff text, recommendation lane alignment, and validation failure for missing artifacts.meta_scan.

## 回帰リスク

Future changes to open-meta artifact keys or supervisor lanes could drift unless steward preflight and lane-result validation tests stay in place.

## フォローアップ

Finalize lane should include IMP0036/E0040/H0040/D0041 in the PR summary; keep FB0045 forgetting policy queued separately.

## 回帰ガード

tests/test_cli/test_steward.py
