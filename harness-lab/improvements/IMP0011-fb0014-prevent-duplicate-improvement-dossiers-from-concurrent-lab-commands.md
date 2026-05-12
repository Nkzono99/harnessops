---
id: IMP0011
record_type: improvement_dossier
created_at: '2026-05-13T02:04:58+09:00'
updated_at: '2026-05-13T02:05:23+09:00'
status: active
source_type: failure
scope: harnessops-core
maturity: investigated
relation: new
promotion_level: target-lab-case
source_feedback: FB0014
eval_cases: []
hypotheses: []
decisions: []
classification:
  capability: lab_record_consistency
  failure_class: duplicate_improvement_dossier_race
guard:
  status: planned
  path: tests/test_cli/test_mvp_flow.py
investigation:
- created_at: '2026-05-13T02:05:22+09:00'
  kind: codebase
  summary: create_or_update_improvement_dossier first scans existing IMP files
    by source_feedback and otherwise allocates next_id from the directory.
    Without locking or duplicate validation, concurrent commands can both miss
    the existing dossier and allocate different IMP IDs. Current doctor
    validates individual records but not uniqueness of source_feedback across
    improvement dossiers.
  evidence_ref: src/harnessops/core/records.py::_find_existing_dossier ;
    src/harnessops/core/records.py::create_or_update_improvement_dossier ;
    src/harnessops/core/validation.py::doctor
links:
  issue_url:
---

# IMP0011: FB0014: Prevent duplicate improvement dossiers from concurrent lab commands

## Status

- status: active
- maturity: investigated
- source_type: failure
- scope: harnessops-core
- relation: new
- promotion_level: target-lab-case
- source_feedback: `FB0014`
- linked_records: `FB0014`

## Source Observation

Source: `harness-lab/records/feedback/FB0014-prevent-duplicate-improvement-dossiers-from-concurrent-lab-commands.md`

# FB0014: Prevent duplicate improvement dossiers from concurrent lab commands

## 概要

Running lab dossier, lab classify, and lab investigate concurrently for the same source feedback created two improvement dossiers for FB0013. Doctor did not detect the duplicate source_feedback mapping.

## 再現

Invoke multiple hops lab commands for a new FB in parallel, such as dossier/classify/investigate. Each command can call create_or_update_improvement_dossier before another command's new dossier is visible, causing duplicate IMP records.

## 期待する上流変更

Make improvement dossier creation idempotent under concurrent calls or add doctor validation that detects duplicate IMP source_feedback values and tells the operator how to repair them.

## Target Capability

- capability: lab_record_consistency
- failure_class: duplicate_improvement_dossier_race

## Investigation

- 2026-05-13T02:05:22+09:00 [codebase] create_or_update_improvement_dossier first scans existing IMP files by source_feedback and otherwise allocates next_id from the directory. Without locking or duplicate validation, concurrent commands can both miss the existing dossier and allocate different IMP IDs. Current doctor validates individual records but not uniqueness of source_feedback across improvement dossiers.

## Evaluation

評価ケースはまだありません。


## Hypotheses

仮説はまだありません。


## Evidence

評価結果はまだありません。

## Guard

- status: planned
- path: tests/test_cli/test_mvp_flow.py

## Links

- issue_url: 未設定

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

## Decision Log

判断レコードはまだありません。
