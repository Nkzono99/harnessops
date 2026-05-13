<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0018

送信元: `harness-lab/records/eval-cases/E0018-fb0018-separate-lab-memory-triggers-from-abstraction.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 4
- minimality: 0
- regression_risk: 0
- operator_burden: 0
- anti_theater: 4
- maintainability: 4
- privacy_sanitization_risk: 0

## メモ

Lint/prepare commands separate trigger detection from semantic abstraction; tests cover nonzero lint, warn-only lint, and input bundle generation.

## 評価ケース

- capability: lab_memory_compaction
- failure_class: deterministic_snapshot_conflates_trigger_and_abstraction
- source_feedback: FB0018
