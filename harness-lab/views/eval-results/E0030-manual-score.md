<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0030

送信元: `harness-lab/records/eval-cases/E0030-fb0031-simplify-harnessops-repository-surfaces.md`

## スコア

- impact: 4
- mechanism_clarity: 4
- evaluability: 5
- minimality: 4
- regression_risk: 2
- operator_burden: 1
- anti_theater: 5
- maintainability: 5
- privacy_sanitization_risk: 0

## メモ

Removed root plugin and user plugin install surfaces, moved packaged agent skills under agent_assets/skills, extracted shared markdown and managed file helpers, demoted experiments from required lab layout, and updated docs/SPEC/README. Verified with ruff check ., pytest -q (92 passed), doctor, and migrate.

## 評価ケース

- capability: repository_maintainability
- failure_class: surface_sprawl
- source_feedback: FB0031
