---
id: FB0055
record_type: imported_feedback
created_at: '2026-05-21T03:12:05+09:00'
status: triaged
source:
  type: harness-feedback-export
  original_id: ISSUE-39
  source_project: redacted
  issue:
    provider: github
    repo: Nkzono99/harnessops
    number: 39
    url: https://github.com/Nkzono99/harnessops/issues/39
    title: update-harness should avoid .gitignore line-ending and whitespace churn
    author: Nkzono99
    labels:
    - bug
    - enhancement
    created_at: '2026-05-20T01:08:47Z'
    updated_at: '2026-05-20T01:08:47Z'
    comments: []
classification:
  failure_class: unclassified
  capability: unclassified
links:
  eval_case:
  issue_url: https://github.com/Nkzono99/harnessops/issues/39
---

# FB0055: update-harness should avoid .gitignore line-ending and whitespace churn

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/39
author: Nkzono99
labels: bug, enhancement
created_at: 2026-05-20T01:08:47Z
updated_at: 2026-05-20T01:08:47Z

## Issue本文
## Summary

Transferred from runops issue #86: https://github.com/Nkzono99/runops/issues/86

After `hops update-harness`, runops observed a large `.gitignore` diff that appeared to be mostly line-ending churn rather than meaningful content change. `git diff --check` also reported trailing whitespace in generated/managed output, requiring manual cleanup.

For managed artifact updates, `.gitignore` and similar existing files should avoid needless line-ending or whitespace churn so reviews focus on real harness changes.

## Expected behavior

When `hops update-harness` touches existing files:

- Preserve the existing line-ending style, or skip the write when normalized content is unchanged.
- Do not emit trailing whitespace from managed templates.
- Detect and report generated/managed whitespace issues after update.

## Acceptance criteria

- If `.gitignore` content is unchanged, update-harness does not produce a large line-ending-only diff.
- Generated or managed files do not introduce trailing whitespace.
- Existing user-managed files receive only minimal real diffs.
- Update summary ideally reports `line ending preserved` or `unchanged due to normalized content match` when applicable.

## Evidence from target repo

In runops on 2026-05-16, `uvx --refresh-package harnessops --from harnessops hops update-harness` produced a large `.gitignore` diff and `git diff --check` flagged trailing whitespace. The runops lab records track this as `FB0012` / `E0012` / `H0012` / `IMP0012`, with decision `D0015` currently `needs-more-evidence` and guard path `harnessops-core:tests/test_harness/test_update_harness.py::test_update_harness_preserves_gitignore_newlines_and_skips_normalized_noop`.

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。
