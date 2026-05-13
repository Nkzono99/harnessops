---
id: D0021
record_type: decision
created_at: '2026-05-13T17:07:31+09:00'
status: adopted
source: H0020
evidence:
  summary: Focused pytest cases and repo-local doctor output showing 0.1.2 -> 0.1.3 notice.
  guard_path: tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_stale_harnessops_lock_once
---

# D0021: adopted H0020

## 判断

adopted

## 理由

Adopted after focused tests and a real stale-lock doctor run confirmed the low-noise update-harness notice behavior.

## 証拠

Focused pytest cases and repo-local doctor output showing 0.1.2 -> 0.1.3 notice.

## 回帰リスク

Low; notice is best-effort, cached for seven days, stderr-only, and suppressed for update-harness/version.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py::test_hops_usage_notices_stale_harnessops_lock_once
