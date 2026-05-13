<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0031

送信元: `harness-lab/records/eval-cases/E0031-fb0032-split-record-core-modules-by-responsibility.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 4
- regression_risk: 2
- operator_burden: 0
- anti_theater: 5
- maintainability: 5
- privacy_sanitization_risk: 0

## メモ

Split records.py into record_types, record_io, record_index, lab_records, and improvement_dossier while keeping records.py as a compatibility facade. Updated internal imports and record schema docs. Verified with ruff check ., pytest -q (92 passed), doctor --check-overlay --check-records, and migrate --check.

## 評価ケース

- capability: repository_maintainability
- failure_class: records_module_sprawl
- source_feedback: FB0032
