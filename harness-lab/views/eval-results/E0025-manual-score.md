<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0025

送信元: `harness-lab/records/eval-cases/E0025-fb0025-separate-open-meta-idea-scan-from-research-routing.md`

## スコア

- impact: 5
- mechanism_clarity: 5
- evaluability: 5
- minimality: 4
- regression_risk: 2
- operator_burden: 2
- anti_theater: 5
- maintainability: 4
- privacy_sanitization_risk: 1

## メモ

Implemented a separate open invention lane: hops-open-meta-scan now produces Raw Ideas, Counterframes, Routing Hints, and Do Not Record Yet without default lab writes; hops-research-improvements now explicitly acts as the downstream selection/routing lane. Repo-local, Codex/Claude plugin, and packaged asset copies are synchronized and guarded by contract tests.

## 評価ケース

- capability: meta_improvement_research
- failure_class: premature_research_routing
- source_feedback: FB0025
