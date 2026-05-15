---
id: FB0042
record_type: imported_feedback
created_at: '2026-05-15T15:11:50+09:00'
status: triaged
source:
  type: local-capture
  original_id:
  source_project: harnessops
classification:
  capability: agent_bridge_distribution
  failure_class: missing_agents_hops_conduit
links:
  eval_case:
  issue_url:
---

# FB0042: Add AGENTS.md HarnessOps conduit guidance to update-harness skill

## 概要

hops-update-harness should help agents notice when AGENTS.md or CLAUDE.md lacks the minimal HarnessOps usage path, while keeping project repos scoped to feedback/lifecycle and target/meta repos scoped to lab/GitHub Flow.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

Add compact AGENTS.md/CLAUDE.md guidance to the update-harness skill and packaged assets, plus contract tests that keep the guidance short and role-aware.
