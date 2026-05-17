---
id: FB0049
record_type: imported_feedback
created_at: '2026-05-17T09:39:00+09:00'
status: triaged
source:
  type: local-capture
  original_id: user request 2026-05-17
  source_project: harnessops
classification:
  capability: daily_steward_orchestration
  failure_class: nested_open_scan_not_delegated
links:
  eval_case:
  issue_url:
---

# FB0049: Daily steward should delegate open meta scan

## 概要

Daily steward supervisor currently lists invention as one lane; hops-open-meta-scan is only nested inside invention guidance, so the supervisor does not spawn a dedicated open-meta-scan subagent or make its raw ideas an explicit handoff into routing and priority work.

## 再現

Run hops steward preflight --json and inspect supervisor_plan.lanes: hops-open-meta-scan is not a lane even though hops-invention-steward mentions it.

## 期待する上流変更

Add an explicit open-meta-scan supervisor lane using hops-open-meta-scan, then make invention review the raw ideas and record selected candidates so priority-improvement-steward can pick them up.
