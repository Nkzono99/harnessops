<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0022

送信元: `harness-lab/records/eval-cases/E0022-fb0022-release-workflow-uses-node20-action-majors.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 5
- regression_risk: 1
- operator_burden: 1
- anti_theater: 5
- maintainability: 4
- privacy_sanitization_risk: 0

## メモ

Updated the PyPI publish workflow to actions/checkout@v5 and actions/setup-python@v6 while preserving the pypi environment, id-token permission, Python 3.11, build, twine check, and publish steps. Added a workflow contract test. Focused test, full pytest, ruff, doctor, and migrate all passed.

## 評価ケース

- capability: harness_lab_traceability
- failure_class: missing_lab_capture
- source_feedback: FB0022
