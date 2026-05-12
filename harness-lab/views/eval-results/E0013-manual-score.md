<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0013

送信元: `harness-lab/records/eval-cases/E0013-fb0014-prevent-duplicate-improvement-dossiers-from-concurrent-lab-commands.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 4
- regression_risk: 3
- operator_burden: 4
- anti_theater: 5
- maintainability: 4
- privacy_sanitization_risk: 5

## メモ

Implemented source_feedback-level locking for dossier creation, doctor validation for duplicate improvement dossier source_feedback values, visible evidence_ref rendering for investigation notes, LF-stable generated records, and canonical record lookup so generated views do not shadow eval cases.

## 評価ケース

- capability: lab_record_consistency
- failure_class: duplicate_improvement_dossier_race
- source_feedback: FB0014
