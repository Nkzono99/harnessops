<!-- harnessops により生成; source records が正本 -->
# 手動評価結果: E0006

送信元: `harness-lab/records/eval-cases/E0006-fb0006-make-update-harness-conflict-aware-for-agent-bridge-files.md`

## スコア

- impact: 4
- mechanism_clarity: 5
- evaluability: 5
- minimality: 4
- regression_risk: 3
- operator_burden: 4
- anti_theater: 5
- maintainability: 4
- privacy_sanitization_risk: 1

## メモ

Implemented conflict-aware agent bridge refresh: managed bridge hashes are stored in lock metadata; unmodified stale files update automatically, local edits produce .new files, --force-agent-bridge overwrites explicitly, and JSON/text output reports checked, updated, unchanged, conflicted, and written_new paths. Verified with focused tests, full pytest, ruff, doctor, and migrate.

## 評価ケース

- capability: unclassified
- failure_class: unclassified
- source_feedback: FB0006
