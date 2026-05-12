---
id: D0005
record_type: decision
created_at: '2026-05-12T19:50:16+09:00'
status: adopted
source: H0003
evidence:
  summary: 'pytest -q: 46 passed; ruff check .: passed; mypy src: passed; hops doctor
    --check-overlay --check-records: ok; hops migrate --check: no pending migrations.'
  guard_path: 
    tests/test_cli/test_safety.py::test_github_issue_draft_requires_strict_sanitize
---

# D0005: adopted H0003

## 判断

adopted

## 理由

Adopt the minimal local GitHub Issue draft workflow rather than remote issue creation in this increment.

## 証拠

pytest -q: 46 passed; ruff check .: passed; mypy src: passed; hops doctor --check-overlay --check-records: ok; hops migrate --check: no pending migrations.

## 回帰リスク

Low to medium: export safety checks changed, guarded by test_github_issue_draft_requires_strict_sanitize and the full CLI suite.

## フォローアップ

Keep #2/#4 open for duplicate search, explicit remote create confirmation, and issue URL write-back.

## 回帰ガード

tests/test_cli/test_safety.py::test_github_issue_draft_requires_strict_sanitize
