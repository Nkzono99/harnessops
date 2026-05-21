---
id: D0046
record_type: decision
created_at: '2026-05-22T03:18:17+09:00'
status: adopted
source: H0045
evidence:
  summary: 'Focused validation passed: uv run pytest tests/test_cli/test_mvp_flow.py -k github_flow_merge -q (5 passed); uv run ruff check src tests passed. Output now keeps pre_merge_pr separate, updates pr/post_merge_pr after successful merge, exposes merged/mergedAt/mergeCommit, and checks deletedBranch.'
  guard_path: tests/test_cli/test_mvp_flow.py::test_github_flow_merge_auto_uses_squash_when_merge_commits_disabled
---

# D0046: adopted H0045

## 判断

adopted

## 理由

Implemented unambiguous post-merge JSON for github-flow merge.

## 証拠

Focused validation passed: uv run pytest tests/test_cli/test_mvp_flow.py -k github_flow_merge -q (5 passed); uv run ruff check src tests passed. Output now keeps pre_merge_pr separate, updates pr/post_merge_pr after successful merge, exposes merged/mergedAt/mergeCommit, and checks deletedBranch.

## 回帰リスク

Low: behavior is scoped to successful merge JSON assembly after existing draft/conflict/check gates and merge method selection.

## フォローアップ

Finalize should include Closes #40 in the PR body after full validation.

## 回帰ガード

tests/test_cli/test_mvp_flow.py::test_github_flow_merge_auto_uses_squash_when_merge_commits_disabled
