---
id: FB0032
record_type: imported_feedback
created_at: '2026-05-14T00:03:20+09:00'
status: triaged
source:
  type: local-capture
  original_id:
  source_project: harnessops
classification:
  capability: repository_maintainability
  failure_class: records_module_sprawl
links:
  eval_case:
  issue_url:
---

# FB0032: Split record core modules by responsibility

## 概要

records.py has become the central maintainability hotspot: it mixes record type constants, frontmatter IO, ID/path indexing, feedback/eval/hypothesis/decision creation, research scan parsing, and improvement dossier aggregation/mutation. Split these responsibilities into focused modules while keeping harnessops.core.records as a compatibility facade.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Introduce record_types.py, record_io.py, record_index.py, lab_records.py, and improvement_dossier.py; preserve current imports and behavior; update tests/docs only where the new structure needs a contract.
