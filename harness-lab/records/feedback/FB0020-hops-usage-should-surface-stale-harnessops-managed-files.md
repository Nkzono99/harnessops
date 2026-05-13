---
id: FB0020
record_type: imported_feedback
created_at: '2026-05-13T17:01:32+09:00'
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

# FB0020: hops usage should surface stale HarnessOps managed files

## 概要

After a HarnessOps release, linked repositories can keep older generated skills or managed artifacts until update-harness runs. Users may keep using hops without noticing that update-harness should be applied.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

When a linked repository is used with a newer hops version than the recorded lock state, hops should emit a low-noise notice that points the user or agent to the hops-update-harness skill / hops update-harness.
