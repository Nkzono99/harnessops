---
id: IMP0007
record_type: improvement_dossier
created_at: '2026-05-13T01:34:18+09:00'
updated_at: '2026-05-13T02:42:07+09:00'
status: adopted
source_type: extension
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: harnessops-protocol
source_feedback: FB0011
eval_cases:
- E0011
hypotheses:
- H0011
decisions:
- D0012
classification:
  capability: meta_hypothesis_scan
  failure_class: missed_second_order_observation
guard:
  status: implemented
  path: tests/test_agent_harness_contract.py
investigation:
- created_at: '2026-05-13T01:34:21+09:00'
  kind: design
  summary: 'The scan should be event-triggered and checkpoint-triggered, but bounded: record only high-signal second-order observations that affect future agent behavior, migration policy, evaluation design, or cross-project promotion.'
  evidence_ref: docs/design-principles.md
links:
  issue_url:
---

# IMP0007: FB0011: Add meta-hypothesis scan harness for autonomous second-order observations

## Status

- status: adopted
- maturity: adopted
- source_type: extension
- scope: harnessops-core
- relation: extends
- promotion_level: harnessops-protocol
- source_feedback: `FB0011`
- linked_records: `FB0011`, `E0011`, `H0011`, `D0012`

## Source Observation

Source: `harness-lab/records/feedback/FB0011-add-meta-hypothesis-scan-harness-for-autonomous-second-order-observations.md`

# FB0011: Add meta-hypothesis scan harness for autonomous second-order observations

## 概要

HarnessOps should help agents notice second-order improvement hypotheses during work, not only when the user explicitly names them. Signals include user interruptions, cross-cutting design principles, repeated friction, migration/compatibility choices, external analogies, and moments where a local idea appears reusable elsewhere.

## 再現

During the standard improvement loop redesign, the user supplied a meta-level compatibility principle mid-work. The agent applied it, but did not autonomously create a separate hypothesis about detecting such second-order observations.

## 期待する上流変更

Define and document a lightweight meta-hypothesis scan harness with trigger signals, checkpoint timing, capture thresholds, outputs, and anti-spam guardrails; update agent lab guidance so the scan runs naturally during substantial work.

## Target Capability

- capability: meta_hypothesis_scan
- failure_class: missed_second_order_observation

## Investigation

- 2026-05-13T01:34:21+09:00 [design] The scan should be event-triggered and checkpoint-triggered, but bounded: record only high-signal second-order observations that affect future agent behavior, migration policy, evaluation design, or cross-project promotion. (evidence: docs/design-principles.md)

## Evaluation

### E0011: E0011: FB0011-add-meta-hypothesis-scan-harness-for-autonomous-second-order-observations を評価


- source: `harness-lab/records/eval-cases/E0011-fb0011-add-meta-hypothesis-scan-harness-for-autonomous-second-order-observations.md`

- capability: meta_hypothesis_scan

- failure_class: missed_second_order_observation

- manual_eval_yml: `harness-lab/views/eval-results/E0011-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0011-manual-score.md`
- scores: impact=5, mechanism_clarity=5, evaluability=4, minimality=4, regression_risk=3, operator_burden=4, anti_theater=4, maintainability=4, privacy_sanitization_risk=1
- notes: Designed the meta-hypothesis scan harness: trigger signals, task checkpoints, output levels, capture thresholds, and anti-spam guardrails are documented in design-principles; run-lab skills now instruct agents to run a bounded scan during interruptions, repeated friction, generalization moments, compatibility/migration decisions, evaluation gaps, and external-comparison discoveries. Verified packaged skill contracts, dossier classification/investigation, full pytest, doctor, and migrate.


## Hypotheses

### H0011: H0011: E0011-fb0011-add-meta-hypothesis-scan-harness-for-autonomous-second-order-observations の仮説


Source: `harness-lab/records/hypotheses/H0011-e0011-fb0011-add-meta-hypothesis-scan-harness-for-autonomous-second-order-observations.md`


# H0011: E0011-fb0011-add-meta-hypothesis-scan-harness-for-autonomous-second-order-observations の仮説

## 仮説

A lightweight meta-hypothesis scan at task boundaries and surprise moments will increase autonomous capture of second-order improvement hypotheses without flooding the lab with loose ideas.

## メカニズム

Define trigger signals, checkpoint timing, capture thresholds, and output levels; encode them in design principles and run-lab skills so agents briefly scan for reusable principles, contradictions, migration decisions, and generalizable friction during substantial work.

## 最小実装

Document the scan harness, update run-lab guidance, classify the resulting dossier as a harnessops-protocol improvement, and test that packaged skills mention the scan.

## 代替案: 削除または統合

Rely on users to explicitly point out every meta-level improvement opportunity.

## 期待される利点

Agents will more often notice that a local implementation decision has broader protocol value and record it while context is fresh.

## 想定される欠点

Over-triggering can create meta-noise and distract from finishing the task.

## 評価計画

Verify docs define triggers/checkpoints/thresholds/outputs; packaged skills instruct agents to run the scan; existing tests and doctor pass.

## 中止基準

If the scan cannot be bounded or anchored to evidence/failure classes, keep it as optional prose rather than a standard harness step.


## Evidence

`harness-lab/views/eval-results/E0011-manual-score.md`

## Guard

- status: implemented
- path: tests/test_agent_harness_contract.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0012: D0012: adopted H0011


Source: `harness-lab/records/decisions/D0012-adopted-h0011.md`


# D0012: adopted H0011

## 判断

adopted

## 理由

H0011 を採用。作業中の二階観測を自律的に拾うため、発火シグナル、チェックポイント、出力レベル、ノイズ抑制を定義し、run-lab skill に標準手順として組み込んだ。

## 証拠

Tests: uv run pytest tests/test_agent_harness_contract.py -k 'lab_capture or packaged_agent_assets'; uv run pytest tests/test_cli/test_mvp_flow.py -k lab_dossier; uv run pytest; uv run ruff check tests/test_agent_harness_contract.py src/harnessops/core/records.py src/harnessops/cli/lab.py src/harnessops/core/render.py src/harnessops/core/validation.py; hops doctor --check-overlay --check-records; hops migrate --check. Manual eval: harness-lab/views/eval-results/E0011-manual-score.yml

## 回帰リスク

Moderate-low. The scan is guidance with bounded output levels, so it should improve capture of high-signal meta observations without requiring a new mandatory record for every thought.

## フォローアップ

Evaluate future sessions for whether agents actually create investigate/classify/capture entries without user prompting when generalizable observations appear.

## 回帰ガード

tests/test_agent_harness_contract.py
