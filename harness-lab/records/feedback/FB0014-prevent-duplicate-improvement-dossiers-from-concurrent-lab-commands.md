---
id: FB0014
record_type: imported_feedback
created_at: '2026-05-13T02:04:48+09:00'
status: triaged
source:
  type: local-capture
  original_id: hops-research-improvements-dry-run-2026-05-13
  source_project: harnessops
classification:
  capability: lab_record_consistency
  failure_class: duplicate_improvement_dossier_race
links:
  eval_case:
  issue_url:
---

# FB0014: Prevent duplicate improvement dossiers from concurrent lab commands

## 概要

Running lab dossier, lab classify, and lab investigate concurrently for the same source feedback created two improvement dossiers for FB0013. Doctor did not detect the duplicate source_feedback mapping.

## 再現

Invoke multiple hops lab commands for a new FB in parallel, such as dossier/classify/investigate. Each command can call create_or_update_improvement_dossier before another command's new dossier is visible, causing duplicate IMP records.

## 期待する上流変更

Make improvement dossier creation idempotent under concurrent calls or add doctor validation that detects duplicate IMP source_feedback values and tells the operator how to repair them.
