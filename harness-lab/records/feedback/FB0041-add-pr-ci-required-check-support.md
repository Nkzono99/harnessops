---
id: FB0041
record_type: imported_feedback
created_at: '2026-05-15T14:39:58+09:00'
status: triaged
source:
  type: local-capture
  original_id:
  source_project: harnessops
classification:
  capability: github_flow_automation
  failure_class: missing_required_check_gate
links:
  eval_case:
  issue_url:
---

# FB0041: Add PR CI required-check support

## 概要

HarnessOps GitHub Flow should have a real PR CI check on GitHub, branch protection should require it, and the merge command should distinguish missing required checks from failing checks.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Add a pull_request CI workflow, improve hops github-flow merge no-check reporting, validate locally, then configure main branch protection to require the PR CI check after the workflow is merged.
