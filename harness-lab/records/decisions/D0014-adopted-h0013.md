---
id: D0014
record_type: decision
created_at: '2026-05-13T02:16:00+09:00'
status: adopted
source: H0013
evidence:
  summary: tests/test_cli/test_mvp_flow.py covers parallel dossier creation,
    duplicate source_feedback doctor failure, and evidence_ref rendering; uv run
    pytest tests/test_cli/test_mvp_flow.py -q; hops doctor --check-overlay
    --check-records
  guard_path: tests/test_cli/test_mvp_flow.py
---

# D0014: adopted H0013

## 判断

adopted

## 理由

The dry-run exposed an actual consistency failure from concurrent lab commands, and the implemented lock plus doctor validation prevents silent duplicate dossiers while preserving the existing dossier workflow.

## 証拠

tests/test_cli/test_mvp_flow.py covers parallel dossier creation, duplicate source_feedback doctor failure, and evidence_ref rendering; uv run pytest tests/test_cli/test_mvp_flow.py -q; hops doctor --check-overlay --check-records

## 回帰リスク

Medium-low: the file lock adds runtime behavior, but it is scoped to source_feedback, has a timeout, and stale lock cleanup.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py
