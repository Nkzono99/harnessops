---
id: FB0048
record_type: imported_feedback
created_at: '2026-05-16T18:20:59+09:00'
status: triaged
source:
  type: harness-feedback-export
  original_id: ISSUE-26
  source_project: redacted
  issue:
    provider: github
    repo: Nkzono99/harnessops
    number: 26
    url: https://github.com/Nkzono99/harnessops/issues/26
    title: update-harness --agent-bridge should clarify or honor [agents].claude
    author: Nkzono99
    labels:
    - documentation
    - enhancement
    created_at: '2026-05-16T05:17:37Z'
    updated_at: '2026-05-16T05:17:46Z'
    comments: []
classification:
  failure_class: unclassified
  capability: unclassified
links:
  eval_case:
  issue_url: https://github.com/Nkzono99/harnessops/issues/26
---

# FB0048: update-harness --agent-bridge should clarify or honor [agents].claude

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/26
author: Nkzono99
labels: documentation, enhancement
created_at: 2026-05-16T05:17:37Z
updated_at: 2026-05-16T05:17:46Z

## Issue本文
## Observation

In a linked target repository (`paperops`), `.harnessops/project.toml` declares both agent bridges as enabled:

```toml
[agents]
codex = true
claude = true
```

After running:

```sh
uvx --refresh-package harnessops --from harnessops hops update-harness --agent-bridge
```

only the Codex-side repo-local HOPS skills under `.agents/skills/` were updated. The Claude-side HOPS bridge was not updated unless `--claude` was passed explicitly.

A dry run showed the latent Claude update clearly:

```sh
uvx --from harnessops hops update-harness --agent-bridge --claude --dry-run
```

That reported `.claude/skills/hops-*` paths as update targets while the `.agents/skills/hops-*` paths were already unchanged.

## Why this is confusing

The project config says `claude = true`, so an operator can reasonably expect `--agent-bridge` to honor that config. If explicit flags are required, the command output or packaged skill docs should make that contract obvious.

## Expected behavior

Either:

- `hops update-harness --agent-bridge` honors `[agents].codex` / `[agents].claude` from `.harnessops/project.toml`, or
- the CLI/docs clearly say that `--codex` / `--claude` must be passed explicitly and that `[agents]` is not used for default bridge selection.

## Validation context

- `uvx --from harnessops hops doctor --check-overlay --check-records`: ok
- `uvx --from harnessops hops migrate --check`: no pending migrations
- repo managed artifacts were already at HarnessOps `0.1.12`

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。
