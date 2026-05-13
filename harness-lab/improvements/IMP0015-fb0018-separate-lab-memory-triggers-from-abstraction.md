---
id: IMP0015
record_type: improvement_dossier
created_at: '2026-05-13T09:19:00+09:00'
updated_at: '2026-05-13T09:28:53+09:00'
status: adopted
source_type: friction
scope: harnessops-core
maturity: adopted
relation: extends
promotion_level: project-pattern
source_feedback: FB0018
eval_cases:
- E0018
hypotheses:
- H0018
decisions:
- D0019
research_scans: []
classification:
  capability: lab_memory_compaction
  failure_class: deterministic_snapshot_conflates_trigger_and_abstraction
guard:
  status: implemented
  path: tests/test_cli/test_mvp_flow.py
investigation:
- created_at: '2026-05-13T09:19:14+09:00'
  kind: codebase
  summary: Existing compact_lab provides deterministic metrics and source-linked lab-memory outputs. Keep it as an index/snapshot, then add memory lint/prepare commands for trigger detection and input bundling while moving higher-level abstraction into an agent skill.
  evidence_ref: src/harnessops/core/lab_compaction.py
links:
  issue_url:
---

# IMP0015: FB0018: Separate lab memory triggers from abstraction

## Status

- status: adopted
- maturity: adopted
- source_type: friction
- scope: harnessops-core
- relation: extends
- promotion_level: project-pattern
- source_feedback: `FB0018`
- linked_records: `FB0018`, `E0018`, `H0018`, `D0019`

## Source Observation

Source: `harness-lab/records/feedback/FB0018-separate-lab-memory-triggers-from-abstraction.md`

# FB0018: Separate lab memory triggers from abstraction

## 概要

Current lab compaction is a deterministic aggregation snapshot, but the desired dream-like behavior needs lint-style trigger checks and a skill-guided abstraction workflow.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Keep source-linked deterministic snapshots as an index, add lint/prepare commands for compaction triggers, and provide an agent skill that performs higher-level lab memory abstraction with source traceability.

## Target Capability

- capability: lab_memory_compaction
- failure_class: deterministic_snapshot_conflates_trigger_and_abstraction

## Investigation

- 2026-05-13T09:19:14+09:00 [codebase] Existing compact_lab provides deterministic metrics and source-linked lab-memory outputs. Keep it as an index/snapshot, then add memory lint/prepare commands for trigger detection and input bundling while moving higher-level abstraction into an agent skill. (evidence: src/harnessops/core/lab_compaction.py)

## Research Scans

research scan はまだありません。


## Evaluation

### E0018: E0018: FB0018-separate-lab-memory-triggers-from-abstraction を評価


- source: `harness-lab/records/eval-cases/E0018-fb0018-separate-lab-memory-triggers-from-abstraction.md`

- capability: lab_memory_compaction

- failure_class: deterministic_snapshot_conflates_trigger_and_abstraction

- manual_eval_yml: `harness-lab/views/eval-results/E0018-manual-score.yml`
- manual_eval_md: `harness-lab/views/eval-results/E0018-manual-score.md`
- scores: impact=4, mechanism_clarity=5, evaluability=4, minimality=0, regression_risk=0, operator_burden=0, anti_theater=4, maintainability=4, privacy_sanitization_risk=0
- notes: Lint/prepare commands separate trigger detection from semantic abstraction; tests cover nonzero lint, warn-only lint, and input bundle generation.


## Hypotheses

### H0018: H0018: E0018-fb0018-separate-lab-memory-triggers-from-abstraction の仮説


Source: `harness-lab/records/hypotheses/H0018-e0018-fb0018-separate-lab-memory-triggers-from-abstraction.md`


# H0018: E0018-fb0018-separate-lab-memory-triggers-from-abstraction の仮説

## 仮説

Separating lab memory lint/prepare from deterministic snapshots lets HarnessOps preserve auditable indexes while allowing agent skills to perform higher-level semantic compaction.

## メカニズム

A non-writing lint command detects pressure and stale/missing memory state; prepare emits a source-linked input bundle; the hops-compact-lab-memory skill updates abstract knowledge with source IDs and source digests.

## 最小実装

Add lab memory lint/prepare CLI paths, a compaction skill, docs, and contract tests while keeping hops lab compact as a deterministic snapshot.

## 代替案: 削除または統合

Remove the deterministic snapshot entirely and rely only on a skill, but that loses cheap machine-readable source indexes and digest checks.

## 期待される利点

紐づく評価ケース `E0018` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。

## 想定される欠点

想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。

## 評価計画

Run targeted CLI and bridge tests, full pytest, ruff, doctor, migrate, and confirm lint/prepare behavior on the live lab.

## 中止基準

Revert or simplify if lint cannot produce actionable triggers, if generated bundles encourage unsourced abstractions, or if the new skill duplicates existing run-lab duties without clearer boundaries.


## Evidence

`harness-lab/views/eval-results/E0018-manual-score.md`

## Guard

- status: implemented
- path: tests/test_cli/test_mvp_flow.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

### D0019: D0019: adopted H0018


Source: `harness-lab/records/decisions/D0019-adopted-h0018.md`


# D0019: adopted H0018

## 判断

adopted

## 理由

The implementation keeps deterministic snapshots as auditable indexes and moves semantic abstraction into an explicit skill workflow.

## 証拠

tests/test_cli/test_mvp_flow.py::test_lab_memory_lint_and_prepare_abstraction_input and tests/test_agent_harness_contract.py verify lint/prepare and skill packaging.

## 回帰リスク

Moderate: this adds another lab memory surface, so docs and skill boundaries must stay clear.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py
