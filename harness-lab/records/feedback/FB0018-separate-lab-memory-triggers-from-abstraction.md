---
id: FB0018
record_type: imported_feedback
created_at: '2026-05-13T09:18:54+09:00'
status: triaged
source:
  type: local-capture
  original_id:
  source_project: harnessops
classification:
  capability: lab_memory_compaction
  failure_class: deterministic_snapshot_conflates_trigger_and_abstraction
links:
  eval_case:
  issue_url:
---

# FB0018: Separate lab memory triggers from abstraction

## 概要

Current lab compaction is a deterministic aggregation snapshot, but the desired dream-like behavior needs lint-style trigger checks and a skill-guided abstraction workflow.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Keep source-linked deterministic snapshots as an index, add lint/prepare commands for compaction triggers, and provide an agent skill that performs higher-level lab memory abstraction with source traceability.
