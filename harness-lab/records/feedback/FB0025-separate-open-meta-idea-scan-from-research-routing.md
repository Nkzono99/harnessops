---
id: FB0025
record_type: imported_feedback
created_at: '2026-05-13T18:49:57+09:00'
status: triaged
source:
  type: local-capture
  original_id:
  source_project: harnessops
classification:
  capability: meta_improvement_research
  failure_class: premature_research_routing
links:
  eval_case:
  issue_url:
---

# FB0025: Separate open meta idea scan from research routing

## 概要

The broad prompt 'meta的な視点で改善案はある?' produces better divergent improvement ideas than the current hops-research-improvements skill because the skill starts with routing, evidence, and record-management constraints. HarnessOps needs a distinct invention lane that preserves open-ended structural critique before lab routing and selection.

## 再現

Compare a normal broad meta prompt with hops-research-improvements on this repository; the broad prompt surfaces more structural design tensions, while the skill funnels toward recordable near-term candidates.

## 期待する上流変更

Add a lightweight open-meta-scan skill that asks for raw divergent ideas without creating records, update hops-research-improvements to consume those raw ideas as the selection/routing lane, and guard packaged skills with contract tests.
