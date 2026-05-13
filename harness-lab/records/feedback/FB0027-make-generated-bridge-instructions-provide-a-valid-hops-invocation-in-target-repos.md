---
id: FB0027
record_type: imported_feedback
created_at: '2026-05-13T22:06:17+09:00'
status: triaged
source:
  type: harness-feedback-export
  original_id: ISSUE-9
  source_project: redacted
  issue:
    provider: github
    repo: Nkzono99/harnessops
    number: 9
    url: https://github.com/Nkzono99/harnessops/issues/9
    title: Make generated bridge instructions provide a valid hops invocation in target repos
    author: Nkzono99
    labels:
    - enhancement
    created_at: '2026-05-12T15:32:51Z'
    updated_at: '2026-05-12T15:32:51Z'
    comments: []
classification:
  failure_class: unclassified
  capability: unclassified
links:
  eval_case:
  issue_url: https://github.com/Nkzono99/harnessops/issues/9
---

# FB0027: Make generated bridge instructions provide a valid hops invocation in target repos

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/9
author: Nkzono99
labels: enhancement
created_at: 2026-05-12T15:32:51Z
updated_at: 2026-05-12T15:32:51Z

## Issue本文
## Context

HarnessOps bridge skills currently tell agents:

```text
PATH に `hops` がない環境では `uv run --with-editable . hops <command>` を使います。
```

This is only correct when the current repository is the HarnessOps checkout. In a linked target repository such as runops, `uv run --with-editable . hops ...` tries to install/run the target project, which does not provide the `hops` console script. During the runops update work, `hops` was not on PATH, so the usable command was instead:

```bash
uv run --with-editable [local HarnessOps checkout path] hops <command>
```

That path knowledge was available to the human/session, but not represented in the project bridge metadata or skill instructions.

## Proposal

Make HarnessOps agent bridge instructions and/or project metadata provide a reliable way to invoke `hops` from target repositories.

Possible approaches:

- Record a `hops_command` or `hops_source` hint in `.harnessops/project.toml` or a generated bridge file.
- Generate bridge skill text that distinguishes between:
  - `hops` installed on PATH
  - HarnessOps checkout available at a known path
  - no local HarnessOps checkout, requiring installation guidance
- Provide a command such as `hops doctor --print-invocation` or `hops bridge command` that emits the recommended invocation for agents.
- Avoid suggesting `uv run --with-editable . hops` in target repositories unless the target actually declares/provides `hops`.

## Why this matters

The bridge is supposed to make target-side agents delegate HarnessOps operations to the CLI. If the fallback invocation is wrong, agents either fail early or bypass HOPS with direct file edits/manual GitHub commands.

## Acceptance criteria

- A linked target repo's generated bridge skill contains a valid fallback command for running HOPS.
- `hops doctor --check-overlay` can detect and warn when the bridge fallback command is not valid for the target repo.
- Tests cover a target repo that does not provide the `hops` console script.

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。
