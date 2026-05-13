---
id: FB0036
record_type: imported_feedback
created_at: '2026-05-14T01:44:28+09:00'
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

# FB0036: Let daily steward use lane budgets and merge automation branches

## 概要

Daily steward currently treats max-systemic-candidates as a single global cap and the recommended prompt stops after pushing an automation branch. User feedback prefers lane-specific budgets, automatic merge when validation passes, optional develop/integration branch workflow, and no direct main push.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Document lane budgets, keep systemic candidates conservative, allow multiple metadata/backfill/read-only items, and update full automation guidance so validated automation branches can be merged into an authorized base or integration branch without direct protected-branch push.
