---
id: FB0052
record_type: imported_feedback
created_at: '2026-05-18T03:06:51+09:00'
status: triaged
source:
  type: harness-feedback-export
  original_id: ISSUE-29
  source_project: redacted
  issue:
    provider: github
    repo: Nkzono99/harnessops
    number: 29
    url: https://github.com/Nkzono99/harnessops/issues/29
    title: Support squash/rebase merge methods in github-flow merge
    author: Nkzono99
    labels:
    - bug
    - enhancement
    created_at: '2026-05-17T00:29:32Z'
    updated_at: '2026-05-17T00:29:32Z'
    comments: []
classification:
  failure_class: unclassified
  capability: unclassified
links:
  eval_case:
  issue_url: https://github.com/Nkzono99/harnessops/issues/29
---

# FB0052: Support squash/rebase merge methods in github-flow merge

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/29
author: Nkzono99
labels: bug, enhancement
created_at: 2026-05-17T00:29:32Z
updated_at: 2026-05-17T00:29:32Z

## Issue本文
## Summary

`hops github-flow merge --require-checks` currently invokes `gh pr merge --merge`. This blocks automation in repositories that intentionally disable merge commits but allow squash or rebase merges.

## Observed

During the paperops daily steward run on 2026-05-17, validation passed and PR #38 was clean:

- Target repo: https://github.com/Nkzono99/paperops
- PR: https://github.com/Nkzono99/paperops/pull/38
- Branch: `codex/steward/20260517-daily`
- Required check: `Smoke / smoke` passed
- `hops github-flow merge --require-checks` failed because the repository disallows merge commits
- Manual workaround: `gh pr merge 38 --repo Nkzono99/paperops --squash --delete-branch`

## Expected

`hops github-flow merge` should support repositories whose allowed merge method is squash or rebase.

Possible shape:

- Add `--method merge|squash|rebase|auto` to `hops github-flow merge`
- Default to `auto` or read the repository's allowed merge methods before choosing
- Preserve `--require-checks` behavior before merging
- Keep protected-branch direct pushes forbidden

## Acceptance criteria

- A repo with merge commits disabled and squash enabled can be merged by HOPS after required checks pass
- A repo with rebase-only policy can be merged by HOPS after required checks pass
- Failure output clearly names the attempted method and the repo policy mismatch
- Existing merge-commit-enabled repos keep working

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。
