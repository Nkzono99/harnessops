<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0021

送信元: `harness-lab/records/eval-cases/E0021-fb0021-packaged-agent-skill-assets-still-document-editable-hops-fallback.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 4
- regression_risk: 2
- operator_burden: 1
- anti_theater: 4
- maintainability: 4
- privacy_sanitization_risk: 1

## メモ

Packaged/generated agent assets now use uvx --from harnessops hops for missing PATH fallback; editable checkout commands remain only in HarnessOps development docs. Contract tests, targeted update-harness tests, full pytest, ruff, doctor, and migrate all passed.

## 評価ケース

- capability: unclassified
- failure_class: unclassified
- source_feedback: FB0021
