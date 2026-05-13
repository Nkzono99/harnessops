---
id: FB0034
record_type: imported_feedback
created_at: '2026-05-14T00:22:48+09:00'
status: triaged
source:
  type: local-capture
  original_id:
  source_project: harnessops
classification:
  capability: repository_maintainability
  failure_class: cli_private_helper_coupling
links:
  eval_case:
  issue_url:
---

# FB0034: Move issue bridge logic out of CLI modules

## 概要

lab.py imports private GitHub issue helpers from feedback.py, coupling two Typer modules. Move shared repo validation, duplicate search, issue creation, and private marker checks into core issue_bridge service.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

feedback and lab issue commands share core issue bridge helpers; CLI modules remain thin and behavior stays unchanged.
