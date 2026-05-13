---
id: FB0019
record_type: imported_feedback
created_at: '2026-05-13T11:44:52+09:00'
status: triaged
source:
  type: local-capture
  original_id: RS0002
  source_project: harnessops
classification:
  capability: generated_view_management
  failure_class: stale_generated_view_repair_gap
links:
  eval_case:
  issue_url:
---

# FB0019: Generated view refresh leaves managed warnings

## 概要

The current lab refresh-views command refreshes dynamic lab views but leaves some doctor-managed generated artifacts stale, so doctor remains ok with generated-view warnings after the apparent repair command.

## 再現

Run hops doctor --check-overlay --check-records, then hops lab refresh-views, then doctor again; README, backlog, and score-trajectory warnings remain.

## 期待する上流変更

Provide a refresh path that updates every doctor-managed lab generated artifact or clearly reports the next repair action, so operators do not learn to ignore stale generated-view warnings.
