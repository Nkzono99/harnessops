---
id: FB0006
record_type: imported_feedback
created_at: '2026-05-12T23:59:30+09:00'
status: triaged
source:
  type: harness-feedback-export
  original_id: ISSUE-6
  source_project: redacted
  issue:
    provider: github
    repo: Nkzono99/harnessops
    number: 6
    url: https://github.com/Nkzono99/harnessops/issues/6
    title: Make update-harness conflict-aware for agent bridge files
    author: Nkzono99
    labels:
    - enhancement
    created_at: '2026-05-12T14:53:22Z'
    updated_at: '2026-05-12T14:53:22Z'
    comments: []
classification:
  failure_class: unclassified
  capability: unclassified
links:
  eval_case:
  issue_url: https://github.com/Nkzono99/harnessops/issues/6
---

# FB0006: Make update-harness conflict-aware for agent bridge files

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/6
author: Nkzono99
labels: enhancement
created_at: 2026-05-12T14:53:22Z
updated_at: 2026-05-12T14:53:22Z

## Issue本文
## Context

While updating runops' HarnessOps bridge, `.agents/skills/hops-export-feedback/SKILL.md` was stale. Running:

```bash
hops update-harness --agent-bridge --codex
```

reported `ok` and `agent bridge: checked 9 paths`, but the stale skill file was not updated because existing skill directories are skipped unless `--force-agent-bridge` is used.

Using `--force-agent-bridge` did update the file, but that is a blunt overwrite mode. It does not distinguish between an unmodified managed file that should be refreshed and a locally edited file that should be preserved.

## Proposal

Make `hops update-harness` conflict-aware for agent bridge files, similar to the behavior expected from `runo update-harness`:

- If a managed file has not been changed locally, overwrite it with the current packaged version.
- If a managed file has local edits, preserve it and write `<path>.new` for the updated packaged version.
- `--force-agent-bridge` should remain available for explicit overwrite.
- JSON and text output should report exact counts and paths for `updated`, `unchanged`, `conflicted`, and `written_new`.
- Agent bridge files should either be tracked in the existing lock metadata or in an equivalent bridge metadata file so stale-but-unmodified files can be detected safely.

## Why this matters

The current behavior can leave target repositories with old HOPS skills while reporting a successful bridge check. In this case, runops kept a stale `hops-export-feedback` skill that said remote issues were not supported, even though HarnessOps had already added `hops feedback issue create`.

## Acceptance criteria

- `hops update-harness --agent-bridge --codex` refreshes an unmodified stale skill without requiring force.
- A locally edited managed skill is not overwritten; a `.new` file is produced instead.
- The command output makes it clear whether files were updated, skipped, or conflicted.
- Tests cover unmodified refresh, local-edit conflict, and forced overwrite.

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。
