<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0007

送信元: `harness-lab/records/eval-cases/E0007-fb0007-simplify-harness-lab-around-per-improvement-dossiers.md`

## スコア

- impact: 4
- mechanism_clarity: 4
- evaluability: 5
- minimality: 4
- regression_risk: 3
- operator_burden: 5
- anti_theater: 4
- maintainability: 4
- privacy_sanitization_risk: 1

## メモ

Implemented lab dossiers as a generated compatibility layer: hops lab dossier --from <FB/E/H/D> creates or updates harness-lab/improvements/IMP*.md from normalized records, refreshes views/improvements.md, preserves FB/E/H/D as the source of truth, and documents when to use the simple dossier versus normalized records. Generated dossiers for FB0001 and FB0006-FB0008 to validate existing issue coverage.

## 評価ケース

- capability: unclassified
- failure_class: unclassified
- source_feedback: FB0007
