<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0023

送信元: `harness-lab/records/eval-cases/E0023-fb0023-research-skill-scope-excludes-linked-target-and-project-repos.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 4
- regression_risk: 2
- operator_burden: 2
- anti_theater: 5
- maintainability: 4
- privacy_sanitization_risk: 2

## メモ

Broadened hops-research-improvements to HarnessOps core plus linked target/project repositories. The skill now branches by repo role: target/meta lab repos use research-scan/investigate/classify/capture/propose, while project repos use failure/feedback/export and must not create harness-lab. Packaged Codex/Claude skill copies, docs, and contract tests were updated. Focused tests, full pytest, ruff, doctor, and migrate all passed.

## 評価ケース

- capability: harness_lab_traceability
- failure_class: missing_lab_capture
- source_feedback: FB0023
