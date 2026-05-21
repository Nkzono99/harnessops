---
id: IMP0042
record_type: improvement_dossier
created_at: '2026-05-22T03:43:18+09:00'
updated_at: '2026-05-22T03:44:01+09:00'
status: adopted
source_type: observation
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: target-lab-case
source_feedback: FB0044
eval_cases:
- E0046
hypotheses:
- H0046
decisions:
- D0047
research_scans: []
classification:
  capability: harness_lab_traceability
  failure_class: missing_lab_capture
guard:
  status: implemented
  path: tests/test_cli/test_steward.py
investigation:
- created_at: '2026-05-22T03:44:01+09:00'
  kind: codebase
  summary: 'RS0009 narrowed this FB0044 extension to daily-steward finalize intent: remote issue/PR/release requests should be durable optional lane-result data rather than prose in recommended_next.'
  evidence_ref: harness-lab/records/research-scans/RS0009-route-finalize-intent-and-remote-bound-privacy.md; src/harnessops/core/steward.py::validate_lane_result
links:
  issue_url:
---

# IMP0042: FB0044: Steward run ledger and lane result validation

## Status

- status: adopted
- maturity: adopted
- source_type: observation
- scope: harnessops-core
- relation: extends
- promotion_level: target-lab-case
- source_feedback: `FB0044`
- linked_records: `FB0044`, `E0046`, `H0046`, `D0047`

## Source Observation

Source: `harness-lab/records/feedback/FB0044-steward-run-ledger-and-lane-result-validation.md`

# FB0044: Steward run ledger and lane result validation

## 概要

The redesigned daily automation now emits a supervisor_plan, but actual lane execution state still lives in agent prose. The supervisor can skip, repeat, or trust malformed lane reports without a durable machine-readable run ledger or lane result validation.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Add HOPS CLI support for starting a steward run ledger, recording lane results against the supervisor_plan contract, validating lane result JSON, and ending a run with auditable status.

## Target Capability

- capability: harness_lab_traceability
- failure_class: missing_lab_capture

## Investigation

- 2026-05-22T03:44:01+09:00 [codebase] RS0009 narrowed this FB0044 extension to daily-steward finalize intent: remote issue/PR/release requests should be durable optional lane-result data rather than prose in recommended_next. (evidence: harness-lab/records/research-scans/RS0009-route-finalize-intent-and-remote-bound-privacy.md; src/harnessops/core/steward.py::validate_lane_result)

## Research Scans

research scan はまだありません。


## Evaluation

### E0046: E0046: FB0044-steward-run-ledger-and-lane-result-validation を評価


- source: `harness-lab/records/eval-cases/E0046-fb0044-steward-run-ledger-and-lane-result-validation.md`

- capability: harness_lab_traceability

- failure_class: missing_lab_capture

- manual_eval_yml: `harness-lab/views/eval-results/E0046-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0046-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=5, minimality=5, regression_risk=3, operator_burden=4, anti_theater=5, maintainability=4, privacy_sanitization_risk=4
- notes: Implemented optional steward lane remote_actions metadata plus validation. Focused guard passed: uv run pytest tests/test_cli/test_steward.py -q (12 passed); uv run ruff check src/harnessops/core/steward.py tests/test_cli/test_steward.py passed.


## Hypotheses

### H0046: H0046: E0046-fb0044-steward-run-ledger-and-lane-result-validation の仮説


Source: `harness-lab/records/hypotheses/H0046-e0046-fb0044-steward-run-ledger-and-lane-result-validation.md`


# H0046: E0046-fb0044-steward-run-ledger-and-lane-result-validation の仮説

## 仮説

Steward lane results should optionally carry typed remote_actions so finalize lanes can discover requested GitHub issue, PR, label, merge, or release actions without scraping prose.

## メカニズム

Expose remote_actions as an optional lane-result field in the supervisor plan, mention it in every lane handoff, and validate each action as a small object with action, target, intent, and optional condition/privacy text.

## 最小実装

Keep the required lane result contract unchanged; add optional remote_actions validation and steward tests for valid and malformed remote-action payloads.

## 代替案: 削除または統合

Continue putting issue closure, PR body, and release intent only in recommended_next prose.

## 期待される利点

Finalize agents can build PR bodies and authorized remote issue actions from durable ledger data while old lanes remain valid when they omit the field.

## 想定される欠点

Lane authors have one more optional field to understand; overly strict action schemas could reject useful future remote intents.

## 評価計画

Run tests/test_cli/test_steward.py and verify validate-lane-result accepts well-formed remote_actions and rejects malformed remote_actions while legacy lane results still pass.

## 中止基準

Reject if the field must become required for all lanes or if validation cannot catch malformed remote action payloads.


## Evidence

`harness-lab/views/eval-results/E0046-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_steward.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0047: D0047: adopted H0046


Source: `harness-lab/records/decisions/D0047-adopted-h0046.md`


# D0047: adopted H0046

## 判断

adopted

## 理由

Optional typed remote_actions extends the existing steward ledger without changing required lane fields, making finalize-facing issue/PR/release intent durable instead of prose-only.

## 証拠

tests/test_cli/test_steward.py validates supervisor-plan exposure, well-formed remote_actions acceptance, malformed remote_actions rejection, and legacy lane-result compatibility.

## 回帰リスク

Future remote action payloads may need richer fields, but unknown extra fields remain allowed and malformed core fields fail validation.

## フォローアップ

Finalize lane should prefer recorded remote_actions when present and can still fall back to prior lane prose for this run's #40 closure.

## 回帰ガード

tests/test_cli/test_steward.py
