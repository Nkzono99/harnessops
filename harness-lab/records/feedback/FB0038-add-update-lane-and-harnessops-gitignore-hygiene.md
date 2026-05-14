---
id: FB0038
record_type: imported_feedback
created_at: '2026-05-14T09:21:37+09:00'
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

# FB0038: Add update lane and HarnessOps gitignore hygiene

## 概要

Daily automation should treat HarnessOps latest/update-harness as a signal-driven update lane, not a mandatory start step. HarnessOps init/link/update-harness should also add a marker-managed .gitignore block for transient HarnessOps files such as .harnessops/cache/.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Document the update lane in daily steward guidance and implement .gitignore block management during init/link/update-harness, preserving user entries and avoiding protected-branch/direct-push side effects.
