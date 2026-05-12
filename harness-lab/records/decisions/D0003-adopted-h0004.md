---
id: D0003
record_type: decision
created_at: '2026-05-12T17:51:02+09:00'
status: adopted
source: H0004
evidence:
  summary: 'Regression test test_update_harness_preserves_dynamic_imported_feedback_view
    plus full pytest suite: 45 passed; hops doctor --check-overlay --check-records
    reports ok.'
  guard_path: tests/test_cli/test_mvp_flow.py
---

# D0003: adopted H0004

## 判断

adopted

## 理由

update-harness now refreshes generated views from source records and preserves managed-file hashes using the same byte-based hash doctor checks.

## 証拠

Regression test test_update_harness_preserves_dynamic_imported_feedback_view plus full pytest suite: 45 passed; hops doctor --check-overlay --check-records reports ok.

## 回帰リスク

Medium-low: generated views remain source-record derived, while edited managed files still produce .new conflict copies.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py
