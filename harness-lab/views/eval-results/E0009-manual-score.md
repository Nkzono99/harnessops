<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0009

送信元: `harness-lab/records/eval-cases/E0009-fb0009-github-issue-import-fails-on-windows-console-decoding.md`

## スコア

- impact: 3
- mechanism_clarity: 5
- evaluability: 5
- minimality: 5
- regression_risk: 2
- operator_burden: 5
- anti_theater: 5
- maintainability: 5
- privacy_sanitization_risk: 1

## メモ

Implemented explicit UTF-8 decoding for gh issue view during feedback import, with replacement on invalid bytes and TypeError fallback handling. Regression test now imports Unicode Japanese issue body/comment and asserts encoding=utf-8 is used. Verified with focused ruff/test, full pytest, doctor, and migrate.

## 評価ケース

- capability: github_issue_import
- failure_class: unicode_decode_failure
- source_feedback: FB0009
