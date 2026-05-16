---
id: FB0044
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

# FB0044: Steward run ledger and lane result validation

## 概要

The redesigned daily automation now emits a supervisor_plan, but actual lane execution state still lives in agent prose. The supervisor can skip, repeat, or trust malformed lane reports without a durable machine-readable run ledger or lane result validation.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Add HOPS CLI support for starting a steward run ledger, recording lane results against the supervisor_plan contract, validating lane result JSON, and ending a run with auditable status.
