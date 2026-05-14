---
id: FB0040
record_type: imported_feedback
created_at: '2026-05-14T11:25:01+09:00'
status: triaged
source:
  type: local-capture
  original_id:
  source_project: harnessops
classification:
  capability: github_flow_automation
  failure_class: hand_rolled_remote_flow
links:
  eval_case:
  issue_url:
---

# FB0040: Standardize GitHub Flow automation for target repos

## 概要

Target repositories should get a standard HOPS GitHub Flow lane so agents do not hand-roll push, PR, merge, conflict, checks, and issue-close behavior. Project repositories should remain lightweight and avoid this clean-flow automation by default.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Add role-aware github_flow config, distribute a hops-github-flow skill only to target/meta/core repos unless disabled, and provide guarded CLI commands for GitHub Flow automation.
