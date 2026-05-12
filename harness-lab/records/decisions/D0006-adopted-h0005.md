---
id: D0006
record_type: decision
created_at: '2026-05-12T20:25:58+09:00'
status: adopted
source: H0005
evidence:
  summary: 'pytest -q: 50 passed; ruff check .: passed; mypy src: passed; hops doctor
    --check-overlay --check-records: ok; hops migrate --check: no pending migrations.'
  guard_path:
    tests/test_cli/test_safety.py::test_feedback_issue_create_writes_back_created_issue_url
---

# D0006: adopted H0005

## 判断

adopted

## 理由

Adopt the first-class GitHub issue bridge helper now that export-side draft, duplicate search, explicit create confirmation, gh fallback, and URL write-back are implemented.

## 証拠

pytest -q: 50 passed; ruff check .: passed; mypy src: passed; hops doctor --check-overlay --check-records: ok; hops migrate --check: no pending migrations.

## 回帰リスク

Medium: command shells out to gh and can create remote issues, but creation requires --confirm-create, duplicates block without --allow-duplicate, and tests cover preview, fallback, validation, and URL write-back.

## フォローアップ

Consider a later convenience wrapper for creating feedback from a failure and exporting in one command; core bridge behavior is now covered.

## 回帰ガード

tests/test_cli/test_safety.py::test_feedback_issue_create_writes_back_created_issue_url
