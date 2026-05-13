---
id: FB0035
record_type: imported_feedback
created_at: '2026-05-14T00:58:08+09:00'
status: triaged
source:
  type: local-capture
  original_id:
  source_project: harnessops
classification:
  capability: daily_steward_orchestration
  failure_class: count_based_preflight_misses_stale_lab_health
links:
  eval_case:
  issue_url:
---

# FB0035: Expose lab health in steward preflight

## 概要

hops steward preflight reports overlay counts and lane triggers, but it does not surface lab memory pressure or stale snapshot/semantic memory state as actionable daily steward input.

## 再現

Run hops steward preflight --json in a meta-lab repository where hops lab memory lint --warn-only reports needs-abstraction; the preflight JSON only shows counts and generic librarian trigger information.

## 期待する上流変更

Steward preflight should include source-linked lab health status and trigger reasons so daily runs can route stale memory or lab pressure to the librarian lane without relying on manual follow-up commands.
