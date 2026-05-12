---
id: FB0013
record_type: imported_feedback
created_at: '2026-05-13T02:03:05+09:00'
status: triaged
source:
  type: local-capture
  original_id: hops-research-improvements-dry-run-2026-05-13
  source_project: harnessops
classification:
  capability: meta_improvement_research
  failure_class: unstructured_research_scan_results
links:
  eval_case:
  issue_url:
---

# FB0013: Structure meta improvement research scan outputs

## 概要

Dry-running the manual meta improvement research skill produced useful candidates, but the result exists only as prose in the agent response or as free-form investigation summaries. HarnessOps lacks a structured research-scan artifact or view for candidate, evidence, relation, recommendation, and next command.

## 再現

Run hops-research-improvements against the current repository. The skill instructs the agent to output Scope, Evidence, Candidates, and Recommendation, but CLI support stops at lab investigate/classify/capture/propose.

## 期待する上流変更

Add a lightweight structured research-scan record or command, for example a lab research/scan artifact that can hold candidates with evidence refs, relation, recommended action, and optional conversion to investigate/capture/propose.
