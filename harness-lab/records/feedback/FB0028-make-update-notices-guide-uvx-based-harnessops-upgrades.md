---
id: FB0028
record_type: imported_feedback
created_at: '2026-05-13T22:11:45+09:00'
status: triaged
source:
  type: local-capture
  original_id: 'user-request: uvx update notice routing'
  source_project: harnessops
classification:
  capability: uvx_update_guidance
  failure_class: stale_hops_update_path
links:
  eval_case:
  issue_url:
---

# FB0028: Make update notices guide uvx-based HarnessOps upgrades

## 概要

Target and project repositories need a single update path when repo-managed HarnessOps artifacts, the currently running hops runtime, and the latest PyPI release differ. The existing notice only compares the repo lock with the current runtime and still points agents at the hops-update-harness skill or bare hops command.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Update the CLI notice so ordinary hops usage in linked repos compares recorded, current, and latest PyPI HarnessOps versions when available, emits uvx --refresh-package harnessops --from harnessops hops update-harness guidance, and keeps migration application behind an explicit follow-up check.
