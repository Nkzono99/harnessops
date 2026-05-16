---
id: FB0045
record_type: imported_feedback
created_at: '2026-05-16T08:53:36+09:00'
status: triaged
source:
  type: local-capture
  original_id:
  source_project: harnessops
classification:
  capability: harness_lab_traceability
  failure_class: missing_lab_capture
links:
  eval_case:
  issue_url:
---

# FB0045: Harness lab needs forgetting policy

## 概要

Harness-lab currently supports recording, deterministic compaction, semantic abstraction, and source-linked extraction, but growth pressure will keep increasing because old low-signal records are never retired, archived, summarized away, or marked out of working memory.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Design a source-preserving forgetting lane that can mark stale local-only or superseded lab material as archived or excluded from active memory without destroying auditability.
