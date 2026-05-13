---
id: FB0022
record_type: imported_feedback
created_at: '2026-05-13T17:54:40+09:00'
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

# FB0022: Release workflow uses Node20 action majors

## 概要

The v0.1.4 PyPI publish workflow succeeded but GitHub Actions annotated the run because actions/checkout@v4 and actions/setup-python@v5 still run on Node.js 20. GitHub plans Node24 default migration on 2026-06-02, so the release workflow should use Node24-ready action majors before this becomes release friction.

## 再現

ローカル改善作業中に観測。

## 期待する上流変更

The PyPI publish workflow should use Node24-ready action majors and a regression test should guard against reintroducing Node20-era checkout/setup-python majors.
