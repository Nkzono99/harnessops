---
id: FB0015
record_type: imported_feedback
created_at: '2026-05-13T02:23:23+09:00'
status: triaged
source:
  type: local-capture
  original_id: implementation-followup-2026-05-13
  source_project: harnessops
classification:
  capability: record_lookup
  failure_class: generated_view_shadowed_record_id
links:
  eval_case:
  issue_url:
---

# FB0015: Prefer canonical records over generated views in record lookup

## 概要

After a manual eval result exists, rerunning hops eval --case E0013 can resolve E0013 to harness-lab/views/eval-results/E0013-manual-score.md instead of the canonical records/eval-cases/E0013 record.

## 再現

Create a manual eval result for E0013, then run hops eval --case E0013 again. find_record scans overlay markdown files broadly and can return the generated eval result view whose record_type is manual_eval_result.

## 期待する上流変更

Make find_record prefer the canonical record directory implied by the ID prefix before falling back to broad overlay lookup, so generated views do not shadow FB/E/H/D/IMP records.
