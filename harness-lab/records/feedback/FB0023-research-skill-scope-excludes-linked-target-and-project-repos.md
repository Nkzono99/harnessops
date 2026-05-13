---
id: FB0023
record_type: imported_feedback
created_at: '2026-05-13T17:59:34+09:00'
status: triaged
source:
  type: local-capture
  original_id:
  source_project: harnessops
classification:
  capability: harness_lab_traceability
  failure_class: missing_lab_capture
links:
  eval_case:
  issue_url:
---

# FB0023: Research skill scope excludes linked target and project repos

## 概要

The hops-research-improvements skill description says it is for HarnessOps meta improvements, which makes it sound like a HarnessOps-core-only tool even though repo-local skills are also deployed into linked target and project repositories. Agents in those repositories should be able to use the same research workflow for target/project harness improvements while preserving the correct lab versus feedback routing.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

The skill and packaged copies should explicitly support HarnessOps core, target repositories with harness-lab, and project repositories with harness-feedback, with guidance for routing research outputs through the right HOPS commands.
