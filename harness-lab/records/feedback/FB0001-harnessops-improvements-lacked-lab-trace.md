---
id: FB0001
record_type: imported_feedback
created_at: '2026-05-12T13:55:01+09:00'
status: triaged
source:
  type: local-capture
  original_id: local-session-2026-05-12
  source_project: harnessops
classification:
  capability: harness_lab_traceability
  failure_class: missing_lab_capture
links:
  eval_case:
  issue_url:
---

# FB0001: HarnessOps improvements lacked lab trace

## 概要

HarnessOps CLI and skill improvements could be implemented, committed, released, and published without any harness-lab record.

## 再現

Run a nontrivial HarnessOps improvement from local conversation without an upstream feedback bundle or GitHub issue. Existing hops-run-lab guidance assumed an FB record already existed.

## 期待する上流変更

Provide a first-class lab capture command and update agent, release, and lab skills so local HarnessOps improvements start with a harness-lab record.
