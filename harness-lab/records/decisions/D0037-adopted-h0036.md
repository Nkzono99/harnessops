---
id: D0037
record_type: decision
created_at: '2026-05-16T18:27:29+09:00'
status: adopted
source: H0036
evidence:
  summary: Focused update-harness tests, packaged skill contract tests, ruff check ., full pytest, doctor, and migrate all passed.
  guard_path: tests/test_cli/test_mvp_flow.py
---

# D0037: adopted H0036

## 判断

adopted

## 理由

update-harness --agent-bridge now honors project [agents] host selection when host flags are omitted, resolving issue #26 while keeping explicit --codex/--claude behavior available.

## 証拠

Focused update-harness tests, packaged skill contract tests, ruff check ., full pytest, doctor, and migrate all passed.

## 回帰リスク

Low: host-selection logic is covered by a new config-driven regression test and existing explicit --codex behavior remains tested.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py
