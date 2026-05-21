<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0046

送信元: `harness-lab/records/eval-cases/E0046-fb0044-steward-run-ledger-and-lane-result-validation.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 5
- regression_risk: 3
- operator_burden: 4
- anti_theater: 5
- maintainability: 4
- privacy_sanitization_risk: 4

## メモ

Implemented optional steward lane remote_actions metadata plus validation. Focused guard passed: uv run pytest tests/test_cli/test_steward.py -q (12 passed); uv run ruff check src/harnessops/core/steward.py tests/test_cli/test_steward.py passed.

## 評価ケース

- capability: harness_lab_traceability
- failure_class: missing_lab_capture
- source_feedback: FB0044
