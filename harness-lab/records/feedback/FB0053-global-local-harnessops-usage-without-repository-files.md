---
id: FB0053
record_type: imported_feedback
created_at: '2026-05-18T14:09:21+09:00'
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

# FB0053: Global local HarnessOps usage without repository files

## 概要

Support a global registry and local state storage so ordinary repositories can use HarnessOps during development without committing .harnessops, harness-feedback, or harness-lab. Agents should access the same flow through a global Codex plugin that delegates all state changes to uvx --from harnessops hops.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Add a global project registry, storage=local overlay resolution, project resolve/link commands, and a packaged/global plugin surface while keeping existing repo-local target/project usage working.
