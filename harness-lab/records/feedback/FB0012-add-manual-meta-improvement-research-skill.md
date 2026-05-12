---
id: FB0012
record_type: imported_feedback
created_at: '2026-05-13T01:40:43+09:00'
status: triaged
source:
  type: local-capture
  original_id: local-design-discussion-2026-05-13
  source_project: harnessops
classification:
  capability: meta_improvement_research
  failure_class: missing_research_skill
links:
  eval_case:
  issue_url:
---

# FB0012: Add manual meta improvement research skill

## 概要

HarnessOps needs a deliberate research skill for meta-level improvement discovery, separate from in-task meta-hypothesis scan. The skill should guide agents through codebase investigation, external web research, comparison, classification, and conversion into lab notes or hypotheses.

## 再現

The user asked for a skill that can be manually triggered to investigate meta-level improvement ideas, including codebase and web research, while still allowing future non-periodic autonomous triggering.

## 期待する上流変更

Add a packaged and repo-local HOPS skill for meta improvement research, with workflow steps, web/source requirements, output thresholds, and lab integration commands.
