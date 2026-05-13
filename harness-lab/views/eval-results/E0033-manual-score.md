<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0033

送信元: `harness-lab/records/eval-cases/E0033-fb0036-let-daily-steward-use-lane-budgets-and-merge-automation-branches.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 4
- regression_risk: 2
- operator_burden: 1
- anti_theater: 5
- maintainability: 4
- privacy_sanitization_risk: 0

## メモ

Updated daily steward docs and repo-local/packaged skill copies to prefer GitHub Flow: automation feature branch, PR, and merge into protected main after validation/required checks. Added lane budgets for systemic candidates, metadata/guard backfills, and read-only park/reject decisions. Updated contract tests to assert the new automation prompt shape. Validation so far: uv run pytest tests/test_agent_harness_contract.py tests/test_cli/test_mvp_flow.py -q (63 passed), uv run ruff check src tests (passed), git diff --check (passed), hops doctor --check-overlay --check-records (ok).

## 評価ケース

- capability: harness_lab_traceability
- failure_class: missing_lab_capture
- source_feedback: FB0036
