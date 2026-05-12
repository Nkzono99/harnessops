---
id: FB0016
record_type: imported_feedback
created_at: '2026-05-13T02:31:50+09:00'
status: triaged
source:
  type: local-capture
  original_id: local-review-2026-05-13
  source_project: harnessops
classification:
  capability: lab_evaluation_review
  failure_class: eval_template_noise_in_dossier
links:
  eval_case:
  issue_url:
---

# FB0016: Remove unused eval-case template noise from dossiers

## 概要

Improvement dossiers render the full eval_case record body under ## Evaluation, so readers see generic sections like fixtures, task, expected behavior, pass/fail criteria that often remain template text. Manual eval yml results are the part that actually functions.

## 再現

Open harness-lab/improvements/IMP*.md and inspect ## Evaluation. It embeds # E000*: ## フィクスチャ, ## タスク, ## 期待される挙動 and similar sections even when they are template text.

## 期待する上流変更

Either make eval cases meaningful in the flow or stop rendering template bodies into dossiers. Prefer summarizing eval records and manual score outputs in dossiers, and generate more source-specific eval case text for new cases.
