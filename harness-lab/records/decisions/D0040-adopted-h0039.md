---
id: D0040
record_type: decision
created_at: '2026-05-18T03:09:52+09:00'
status: adopted
source: H0039
evidence:
  summary: uv run pytest tests/test_cli/test_mvp_flow.py; uv run ruff check src/harnessops/cli/github_flow.py tests/test_cli/test_mvp_flow.py
  guard_path: tests/test_cli/test_mvp_flow.py
---

# D0040: adopted H0039

## 判断

adopted

## 理由

github-flow merge can now choose repository-compatible merge methods while preserving required-check and conflict gates.

## 証拠

uv run pytest tests/test_cli/test_mvp_flow.py; uv run ruff check src/harnessops/cli/github_flow.py tests/test_cli/test_mvp_flow.py

## 回帰リスク

Low: command behavior remains gated by gh pr view/checks and existing merge repositories are handled through auto selecting merge when allowed.

## フォローアップ

変更を昇格する前にこの判断をレビューしてください。

## 回帰ガード

tests/test_cli/test_mvp_flow.py
