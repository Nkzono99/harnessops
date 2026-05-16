---
id: FB0046
record_type: imported_feedback
created_at: '2026-05-16T09:52:51+09:00'
status: triaged
source:
  type: local-capture
  original_id:
  source_project: harnessops
classification:
  capability: harness_lab_traceability
  failure_class: records_without_reuse_path
links:
  eval_case:
  issue_url:
---

# FB0046: Lab records need first-class reuse commands

## 概要

Harness-lab can capture, evaluate, compact, and archive records, but agents still rely on ad hoc reading to select work or retrieve relevant prior decisions.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Provide CLI commands that expose ranked lab queues, contextual recall, and lifecycle lint findings so daily steward lanes use records as working memory.
