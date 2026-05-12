<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0008

送信元: `harness-lab/records/eval-cases/E0008-fb0008-add-github-issue-workflow-for-lab-first-improvement-records.md`

## スコア

- impact: 4
- mechanism_clarity: 4
- evaluability: 5
- minimality: 4
- regression_risk: 3
- operator_burden: 4
- anti_theater: 5
- maintainability: 4
- privacy_sanitization_risk: 2

## メモ

Implemented lab-first GitHub issue promotion: hops lab issue draft/create --from <FB/E/H/D/IMP> builds a sanitized issue body from the generated dossier, writes local markdown drafts, searches duplicates, requires --confirm-create for remote creation, and writes the created URL back to the dossier plus source feedback. Verified sanitizer, draft, duplicate-safe create, URL writeback, help, full pytest, doctor, and migrate.

## 評価ケース

- capability: unclassified
- failure_class: unclassified
- source_feedback: FB0008
