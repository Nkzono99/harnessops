---
id: FB0030
record_type: imported_feedback
created_at: '2026-05-13T23:10:55+09:00'
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

# FB0030: Chain HarnessOps updates through version checkpoints

## 概要

uvx を標準導線にしたことで、target/project repo の update-harness は最新 PyPI runtime から開始できる。古い managed artifact への互換コードを永久に持つ代わりに、lock の harnessops_version から公開済み checkpoint を計画し、必要な版を uvx で順に呼び出す更新チェーンを追加する。

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

hops update-harness が chain plan/apply の導線を提供し、update skill が通常更新と段階更新を使い分けられるようになる。
