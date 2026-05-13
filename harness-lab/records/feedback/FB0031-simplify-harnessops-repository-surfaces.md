---
id: FB0031
record_type: imported_feedback
created_at: '2026-05-13T23:34:05+09:00'
status: triaged
source:
  type: local-capture
  original_id:
  source_project: harnessops
classification:
  capability: repository_maintainability
  failure_class: surface_sprawl
links:
  eval_case:
  issue_url:
---

# FB0031: Simplify HarnessOps repository surfaces

## 概要

HarnessOps has grown through feature work: root plugin artifacts may no longer be part of the standard path, core modules mix workflow logic with small utility boundaries, harness-lab contains directories with weak or missing workflows, and docs/SPEC/README may not reflect recent CLI and uvx update-chain behavior. Clean up repo surfaces and improve maintainability without changing core behavior.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Remove or retire obsolete plugin surfaces, add low-risk code organization boundaries, document current standard workflows, and record any lab layout cleanup as a deliberate migration path rather than ad hoc file moves.
