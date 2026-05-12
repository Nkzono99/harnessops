---
id: FB0008
record_type: imported_feedback
created_at: '2026-05-13T00:00:15+09:00'
status: triaged
source:
  type: harness-feedback-export
  original_id: ISSUE-8
  source_project: redacted
  issue:
    provider: github
    repo: Nkzono99/harnessops
    number: 8
    url: https://github.com/Nkzono99/harnessops/issues/8
    title: Add GitHub issue workflow for lab-first improvement records
    author: Nkzono99
    labels:
    - enhancement
    created_at: '2026-05-12T14:54:12Z'
    updated_at: '2026-05-12T14:54:12Z'
    comments: []
classification:
  failure_class: unclassified
  capability: unclassified
links:
  eval_case:
  issue_url: https://github.com/Nkzono99/harnessops/issues/8
---

# FB0008: Add GitHub issue workflow for lab-first improvement records

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/8
author: Nkzono99
labels: enhancement
created_at: 2026-05-12T14:54:12Z
updated_at: 2026-05-12T14:54:12Z

## Issue本文
## Context

HarnessOps now has `hops feedback issue create` for sanitized exported feedback bundles. That is useful for project-side feedback records.

However, in the current runops workflow we captured a HarnessOps improvement directly via:

```bash
hops lab capture ...
hops lab new-eval-case --from FB0001
hops propose --from E0001
```

When asked to create a GitHub issue from that lab-first record, `hops feedback export --target harnessops --sanitize --format github-issue` did not find a matching project-side feedback bundle. We had to create the GitHub issue manually with `gh issue create`.

This is a gap for the lab-first improvement workflow proposed in #5.

## Proposal

Add a first-class path from `harness-lab` records to GitHub Issue drafts/creation.

Possible command shapes:

```bash
hops lab issue draft --from FB0001
hops lab issue create --from FB0001 --repo owner/repo --confirm-create
```

or:

```bash
hops feedback issue create --from-lab FB0001 --repo owner/repo --confirm-create
```

Expected behavior:

- Build an issue title/body from a lab record or improvement dossier.
- Require sanitized/public-safe content for remote issue creation.
- Print the title/body and duplicate candidates before creating anything.
- Require `--confirm-create` for remote creation.
- Write the resulting Issue URL back to the source lab record.
- Support records created by `hops lab capture`, not only exported project feedback bundles.

## Why this matters

If HarnessOps wants agents to capture non-issue-driven improvements in `harness-lab`, those records also need a smooth promotion path to the external task tracker. Otherwise the lab becomes a side notebook that must be manually retyped into GitHub Issues.

## Related

- #4 added GitHub issue helpers for exported feedback workflows.
- #5 proposes a generic improve-harness workflow in HarnessOps.
- #7 discusses simplifying `harness-lab` around per-improvement dossiers.

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。
