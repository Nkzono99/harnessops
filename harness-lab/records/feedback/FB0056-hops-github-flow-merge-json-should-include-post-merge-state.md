---
id: FB0056
record_type: imported_feedback
created_at: '2026-05-22T03:13:24+09:00'
status: triaged
source:
  type: harness-feedback-export
  original_id: ISSUE-40
  source_project: redacted
  issue:
    provider: github
    repo: Nkzono99/harnessops
    number: 40
    url: https://github.com/Nkzono99/harnessops/issues/40
    title: hops github-flow merge --json should include post-merge state
    author: Nkzono99
    labels:
    - enhancement
    created_at: '2026-05-20T01:08:49Z'
    updated_at: '2026-05-20T01:08:49Z'
    comments: []
classification:
  failure_class: unclassified
  capability: unclassified
links:
  eval_case:
  issue_url: https://github.com/Nkzono99/harnessops/issues/40
---

# FB0056: hops github-flow merge --json should include post-merge state

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/40
author: Nkzono99
labels: enhancement
created_at: 2026-05-20T01:08:49Z
updated_at: 2026-05-20T01:08:49Z

## Issue本文
## Summary

Transferred from runops issue #88: https://github.com/Nkzono99/runops/issues/88

`hops github-flow merge --json` has returned PR information captured before merge, so `pr.state` can remain `OPEN` even when the merge command itself succeeded. Finalization lanes then need an extra `gh pr view --json state,mergedAt,mergeCommit` call to build a reliable final report.

The merge command should return machine-readable post-merge state directly.

## Expected JSON fields

Possible fields:

- `merged: true|false`
- `pr.number`, `pr.url`, `pr.state`
- `mergedAt`
- `mergeCommit.oid`
- `headRefName`, `baseRefName`
- `deletedBranch: true|false`
- `checksSummary`
- if both snapshots are useful, distinguish them as `pre_merge_pr` and `post_merge_pr`

## Acceptance criteria

- After a successful merge, JSON indicates `state=MERGED` or `merged=true`.
- Merge commit SHA is available from JSON.
- Branch deletion success/failure is available from JSON.
- Pre-merge and post-merge snapshots are not mixed under ambiguous field names.
- Automation can produce its final report without a second `gh pr view` call.

## Evidence from target repo

During a runops steward run, `hops github-flow merge 83 --require-checks --delete-branch --json` succeeded, but returned `pr.state` from the pre-merge snapshot. The runops lab records track this as `FB0014` / `E0014` / `H0014` / `IMP0014`, with decision `D0014` currently `needs-more-evidence`.

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。
