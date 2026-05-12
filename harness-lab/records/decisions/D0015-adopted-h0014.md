---
id: D0015
record_type: decision
created_at: '2026-05-13T02:26:44+09:00'
status: adopted
source: H0014
evidence:
  summary: tests/test_cli/test_mvp_flow.py reruns eval by ID after E0001-manual-score.md exists; uv run pytest tests/test_cli/test_mvp_flow.py -q
  guard_path: tests/test_cli/test_mvp_flow.py
---

# D0015: adopted H0014

## 判断

adopted

## 理由

Generated views can share ID prefixes with canonical records, so prefix-directed lookup is needed to keep ordinary commands like hops eval --case E0013 stable after views exist.

## 証拠

tests/test_cli/test_mvp_flow.py reruns eval by ID after E0001-manual-score.md exists; uv run pytest tests/test_cli/test_mvp_flow.py -q

## 回帰リスク

Low: path-based lookup still works first, and prefix routing falls back to broad overlay lookup when no canonical record exists.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py
