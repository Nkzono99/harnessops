---
id: FB0043
record_type: imported_feedback
created_at: '2026-05-16T07:59:08+09:00'
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

# FB0043: Redesign daily steward as supervisor lanes

## 概要

Daily automation is currently strong but monolithic: reactive maintenance, lab cleanup, issue triage, invention, priority improvement execution, and finalization compete inside one large skill, so small safe work often satisfies the run before all intended lanes execute. Redesign the daily flow as a thin supervisor plus small lane skills with explicit sequential subagent handoffs and compact lane result contracts.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Replace the monolithic daily steward prompt/skill with a concise supervisor contract and separate maintenance, issue execution, invention, priority improvement, and finalize lane skills so a single automation can run all lanes without prompt bloat or skipped steps.
