---
id: D0017
record_type: decision
created_at: '2026-05-13T03:10:44+09:00'
status: adopted
source: H0016
evidence:
  summary: Focused tests cover forced compaction, threshold skipping, source-linked capability knowledge, score summaries, guard index, Curator Notes preservation, and doctor compatibility.
  guard_path: tests/test_cli/test_mvp_flow.py
---

# D0017: adopted H0016

## 判断

adopted

## 理由

The implementation gives harness-lab a threshold-gated compaction path that preserves records and creates a mutable, source-linked knowledge layer for long-running labs.

## 証拠

Focused tests cover forced compaction, threshold skipping, source-linked capability knowledge, score summaries, guard index, Curator Notes preservation, and doctor compatibility.

## 回帰リスク

Moderate: summaries can become stale or over-trusted, mitigated by source IDs, source digest, no record deletion, and tests that preserve the source-linked contract.

## フォローアップ

Use hops lab compact --force after large lab updates or release-prep reviews; later work can add doctor warnings or automation around stale knowledge.

## 回帰ガード

tests/test_cli/test_mvp_flow.py
