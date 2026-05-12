<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0014

送信元: `harness-lab/records/eval-cases/E0014-fb0015-prefer-canonical-records-over-generated-views-in-record-lookup.md`

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

find_record now searches the canonical record directory implied by known ID prefixes before broad overlay lookup. Regression test reruns eval by ID after an eval result view exists.

## 評価ケース

- capability: record_lookup
- failure_class: generated_view_shadowed_record_id
- source_feedback: FB0015
