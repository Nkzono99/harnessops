---
id: FB0037
record_type: imported_feedback
created_at: '2026-05-14T09:03:05+09:00'
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

# FB0037: Compact daily steward automation around risk budgets

## 概要

Daily steward automation guidance is too long and conservative: docs still present a recommended weak prompt, max-systemic-candidates encourages status-only no-op, and discovery is gated too tightly for strong unattended automation.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Replace daily steward guidance with a compact strong automation contract: risk-tier/work-packet budgets, proactive discovery/no-idle policy, gate levels split by record/implementation/merge, and a single strong docs prompt with PR/merge/issue/release authority.
