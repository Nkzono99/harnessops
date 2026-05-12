---
id: FB0011
record_type: imported_feedback
created_at: '2026-05-13T01:33:47+09:00'
status: triaged
source:
  type: local-capture
  original_id: local-design-discussion-2026-05-13
  source_project: harnessops
classification:
  capability: meta_hypothesis_scan
  failure_class: missed_second_order_observation
links:
  eval_case:
  issue_url:
---

# FB0011: Add meta-hypothesis scan harness for autonomous second-order observations

## 概要

HarnessOps should help agents notice second-order improvement hypotheses during work, not only when the user explicitly names them. Signals include user interruptions, cross-cutting design principles, repeated friction, migration/compatibility choices, external analogies, and moments where a local idea appears reusable elsewhere.

## 再現

During the standard improvement loop redesign, the user supplied a meta-level compatibility principle mid-work. The agent applied it, but did not autonomously create a separate hypothesis about detecting such second-order observations.

## 期待する上流変更

Define and document a lightweight meta-hypothesis scan harness with trigger signals, checkpoint timing, capture thresholds, outputs, and anti-spam guardrails; update agent lab guidance so the scan runs naturally during substantial work.
