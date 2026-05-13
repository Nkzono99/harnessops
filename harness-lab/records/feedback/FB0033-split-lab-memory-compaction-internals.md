---
id: FB0033
record_type: imported_feedback
created_at: '2026-05-14T00:22:18+09:00'
status: triaged
source:
  type: local-capture
  original_id:
  source_project: harnessops
classification:
  capability: repository_maintainability
  failure_class: lab_compaction_module_sprawl
links:
  eval_case:
  issue_url:
---

# FB0033: Split lab memory compaction internals

## 概要

lab_compaction.py remains broad after record module cleanup. Split its metrics, source collection, lint/prepare, and rendering responsibilities into focused modules while keeping the public compact/lint/prepare API stable.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Smaller lab memory modules with unchanged CLI behavior and passing compact/lint/prepare tests.
