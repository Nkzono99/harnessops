<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0019

送信元: `harness-lab/records/eval-cases/E0019-fb0019-generated-view-refresh-leaves-managed-warnings.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 5
- regression_risk: 2
- operator_burden: 5
- anti_theater: 5
- maintainability: 4
- privacy_sanitization_risk: 5

## メモ

Implemented lab refresh-views so it first refreshes doctor-managed overlay artifacts, then regenerates dynamic lab views with deduplicated output. Focused regression covers stale README/backlog/score-trajectory lock warnings and preserves research-scan view content; doctor now reports ok without generated-view warnings.

## 評価ケース

- capability: generated_view_management
- failure_class: stale_generated_view_repair_gap
- source_feedback: FB0019
