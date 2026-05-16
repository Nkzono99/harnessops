---
id: FB0047
record_type: imported_feedback
created_at: '2026-05-16T10:15:55+09:00'
status: triaged
source:
  type: local-capture
  original_id:
  source_project: harnessops
classification:
  capability: cli_ergonomics
  failure_class: command_surface_sprawl
links:
  eval_case:
  issue_url:
---

# FB0047: CLI surface needs canonical grouped commands

## 概要

HarnessOps CLI now exposes several lifecycle actions as top-level or parallel lab commands, making the recommended path harder to learn and increasing automation ambiguity.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Group feedback actions under feedback, lab evaluation actions under lab, review actions under lab review, memory compaction under lab memory, and emit deprecation warnings from old entrypoints.
