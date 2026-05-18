---
id: D0042
record_type: decision
created_at: '2026-05-19T03:33:01+09:00'
status: adopted
source: H0041
evidence:
  summary: Focused pytest passed for tests/test_cli/test_lab_usage.py, covering preserved source record, retirement metadata, active queue exclusion, include-closed visibility, and memory abstraction input exclusion.
  guard_path: tests/test_cli/test_lab_usage.py::test_lab_retire_preserves_record_and_excludes_active_queue_and_memory
---

# D0042: adopted H0041

## 判断

adopted

## 理由

Adopt the narrow retire primitive because it solves the active queue and semantic memory part of FB0045 without deleting records or adding a broad cleanup lane.

## 証拠

Focused pytest passed for tests/test_cli/test_lab_usage.py, covering preserved source record, retirement metadata, active queue exclusion, include-closed visibility, and memory abstraction input exclusion.

## 回帰リスク

Low to medium: retired records may be hidden from default active context, mitigated by preserving the source file, retirement metadata, and --include-closed queue visibility.

## フォローアップ

Use retire only for stale or superseded queue records with explicit evidence; physical deletion remains release-gated archive work.

## 回帰ガード

tests/test_cli/test_lab_usage.py::test_lab_retire_preserves_record_and_excludes_active_queue_and_memory
