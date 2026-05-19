---
id: FB0054
record_type: imported_feedback
created_at: '2026-05-20T03:11:29+09:00'
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
    updated_at: '2026-05-19T17:00:55Z'
    comments:
    - author: Nkzono99
      created_at: '2026-05-19T17:00:54Z'
      body: "Reopening because the same failure recurred in the next paperops steward run.\n\n## New occurrence\n\n- Target repo: https://github.com/Nkzono99/paperops\n- PR: https://github.com/Nkzono99/paperops/pull/41\n- Branch: `codex/steward/20260519-daily`\n- Commit: `3ede1612e3bdf6b0f5ab8ded225076a6a03c6476`\n- Required check: `Smoke / smoke` passed\n- PR merge state: `CLEAN`\n- Failing command: `hops github-flow merge --require-checks`\n- Failure mode: the command attempted `gh pr merge --merge`, but the repository rejects merge commits.\n\nManual workaround requested for paperops: squash merge PR #41.\n\nThis means the earlier issue is still observable from a target repository using the current steward path. The desired behavior remains: `hops github-flow merge` should support squash/rebase or auto-detect an allowed merge method while preserving required-check gating.\r\n"
classification:
  failure_class: unclassified
  capability: unclassified
links:
  eval_case:
  issue_url: https://github.com/Nkzono99/harnessops/issues/29
---

# FB0054: Support squash/rebase merge methods in github-flow merge

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/29
author: Nkzono99
labels: bug, enhancement
created_at: 2026-05-17T00:29:32Z
updated_at: 2026-05-19T17:00:55Z

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

## コメント
### Comment 1: Nkzono99
Reopening because the same failure recurred in the next paperops steward run.

## New occurrence

- Target repo: https://github.com/Nkzono99/paperops
- PR: https://github.com/Nkzono99/paperops/pull/41
- Branch: `codex/steward/20260519-daily`
- Commit: `3ede1612e3bdf6b0f5ab8ded225076a6a03c6476`
- Required check: `Smoke / smoke` passed
- PR merge state: `CLEAN`
- Failing command: `hops github-flow merge --require-checks`
- Failure mode: the command attempted `gh pr merge --merge`, but the repository rejects merge commits.

Manual workaround requested for paperops: squash merge PR #41.

This means the earlier issue is still observable from a target repository using the current steward path. The desired behavior remains: `hops github-flow merge` should support squash/rebase or auto-detect an allowed merge method while preserving required-check gating.

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。
