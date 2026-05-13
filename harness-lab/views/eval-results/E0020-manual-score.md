<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0020

送信元: `harness-lab/records/eval-cases/E0020-fb0020-hops-usage-should-surface-stale-harnessops-managed-files.md`

## スコア

- impact: 4
- mechanism_clarity: 4
- evaluability: 5
- minimality: 4
- regression_risk: 2
- operator_burden: 1
- anti_theater: 4
- maintainability: 4
- privacy_sanitization_risk: 1

## メモ

Focused regression tests show stale harnessops_version emits a hops-update-harness notice once and suppresses it for update-harness itself; a real doctor run in this repository surfaced the stale 0.1.2 -> 0.1.3 lock.

## 評価ケース

- capability: harness_lab_traceability
- failure_class: missing_lab_capture
- source_feedback: FB0020
