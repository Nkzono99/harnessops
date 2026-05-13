<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0027

送信元: `harness-lab/records/eval-cases/E0027-fb0027-make-generated-bridge-instructions-provide-a-valid-hops-invocation-in-target-repos.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 4
- regression_risk: 2
- operator_burden: 1
- anti_theater: 4
- maintainability: 4
- privacy_sanitization_risk: 2

## メモ

Doctor now warns when a target repo bridge contains the stale editable fallback and the repo does not declare a local hops console script. Focused positive/negative tests, full pytest, ruff, doctor, and migrate passed.

## 評価ケース

- capability: unclassified
- failure_class: unclassified
- source_feedback: FB0027
