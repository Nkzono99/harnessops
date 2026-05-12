---
id: FB0010
record_type: imported_feedback
created_at: '2026-05-13T00:50:17+09:00'
status: triaged
source:
  type: local-capture
  original_id: local-design-discussion-2026-05-13
  source_project: harnessops
classification:
  capability: improvement_loop_design
  failure_class: ambiguous_improvement_workflow
links:
  eval_case:
  issue_url:
---

# FB0010: Redesign standard improvement loop around investigation and themes

## 概要

The current design-principles standard improvement loop is too abstract: observation, routing, guard, and promotion are unclear, and it does not explicitly include investigation, external comparison, improvement classification, theme maturity, or later contradictory/extension observations.

## 再現

While reviewing docs/design-principles.md, the loop leaves agents unsure whether observation includes issues/friction/external research, whether routing means periodic review or classification, what guard means, and how promotion should be designed.

## 期待する上流変更

Define a concrete improvement-loop vocabulary and add lightweight harness support so agents naturally capture observations, investigation notes, classification, theme status, relations, guards, and promotion levels before implementation and review.
