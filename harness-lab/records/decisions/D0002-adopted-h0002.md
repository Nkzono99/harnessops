---
id: D0002
record_type: decision
created_at: '2026-05-12T17:50:40+09:00'
status: adopted
source: H0002
evidence:
  summary: 'Regression test test_paper_harness_upstream_manifest_uses_pops plus full
    pytest suite: 45 passed.'
  guard_path: tests/test_cli/test_mvp_flow.py
---

# D0002: adopted H0002

## 判断

adopted

## 理由

paper-harness-upstream manifest commands now follow the current paperops/pops CLI surface without changing the project-side paper-harness profile.

## 証拠

Regression test test_paper_harness_upstream_manifest_uses_pops plus full pytest suite: 45 passed.

## 回帰リスク

Low: change is scoped to the paper-harness-upstream profile branch in manifest generation.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py
