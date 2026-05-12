<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0003

送信元: `harness-lab/records/eval-cases/E0003-fb0003-github-issue-2.md`

## スコア

- impact: 3
- mechanism_clarity: 4
- evaluability: 4
- minimality: 4
- regression_risk: 2
- operator_burden: 3
- anti_theater: 4
- maintainability: 4
- privacy_sanitization_risk: 1

## メモ

Implemented the minimal sanitized GitHub issue draft path: feedback export --sanitize --format github-issue writes a local markdown draft, refuses unsanitized issue drafts, and refuses --allow-private for public issue draft format. Remote issue creation, duplicate search, and URL write-back remain follow-up.

## 評価ケース

- capability: unclassified
- failure_class: unclassified
- source_feedback: FB0003
