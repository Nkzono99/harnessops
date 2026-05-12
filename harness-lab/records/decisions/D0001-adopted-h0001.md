---
id: D0001
record_type: decision
created_at: '2026-05-12T13:55:22+09:00'
status: adopted
source: H0001
evidence:
  summary: See harness-lab/views/eval-results/E0001-manual-score.yml and
    tests/test_cli/test_mvp_flow.py::test_lab_capture_records_local_improvement.
  guard_path: tests/test_cli/test_mvp_flow.py
---

# D0001: adopted H0001

## 判断

adopted

## 理由

The missing trace was caused by a weak first-step workflow, not by absent storage. A dedicated capture command plus skill and release guidance closes that gap with minimal new surface.

## 証拠

See harness-lab/views/eval-results/E0001-manual-score.yml and tests/test_cli/test_mvp_flow.py::test_lab_capture_records_local_improvement.

## 回帰リスク

Low. The new command only writes harness-lab records in upstream-lab/meta-lab modes and reuses existing record validation.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py
