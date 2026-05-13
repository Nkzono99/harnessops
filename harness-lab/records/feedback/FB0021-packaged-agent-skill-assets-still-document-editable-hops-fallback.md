---
id: FB0021
record_type: imported_feedback
created_at: '2026-05-13T17:15:08+09:00'
status: triaged
source:
  type: harness-feedback-export
  original_id: ISSUE-10
  source_project: redacted
  issue:
    provider: github
    repo: Nkzono99/harnessops
    number: 10
    url: https://github.com/Nkzono99/harnessops/issues/10
    title: Packaged agent SKILL assets still document editable hops fallback
    author: Nkzono99
    labels: []
    created_at: '2026-05-13T08:01:45Z'
    updated_at: '2026-05-13T08:01:45Z'
    comments: []
classification:
  failure_class: unclassified
  capability: unclassified
links:
  eval_case:
  issue_url: https://github.com/Nkzono99/harnessops/issues/10
---

# FB0021: Packaged agent SKILL assets still document editable hops fallback

## 概要

GitHub issue: https://github.com/Nkzono99/harnessops/issues/10
author: Nkzono99
labels: なし
created_at: 2026-05-13T08:01:45Z
updated_at: 2026-05-13T08:01:45Z

## Issue本文
## Summary

The packaged HarnessOps agent assets still tell agents to use an editable local checkout fallback:

```text
uv run --with-editable . hops <command>
```

Current HarnessOps docs for target/project integration already assume the PyPI package path, so linked downstream repositories should be guided toward the PyPI-installed CLI instead, for example:

```text
uvx --from harnessops hops <command>
```

## Observed from downstream update

While updating a linked downstream repository with PyPI `harnessops==0.1.3`, the repo-local agent SKILL copies had to be adjusted from editable fallback to PyPI/`uvx` fallback.

## Affected upstream assets

`rg "uv run --with-editable|with-editable"` shows at least:

- `src/harnessops/core/agent_bridge.py`
- `src/harnessops/agent_assets/plugins/codex/harnessops/skills/hops-compact-lab-memory/SKILL.md`
- `src/harnessops/agent_assets/plugins/claude/harnessops/skills/hops-compact-lab-memory/SKILL.md`
- `src/harnessops/agent_assets/plugins/codex/harnessops/README.md`
- `src/harnessops/agent_assets/plugins/claude/harnessops/README.md`

## Desired behavior

- Packaged Codex/Claude SKILL assets should match the PyPI distribution model documented in `docs/`.
- When `hops` is not on `PATH`, agent instructions should prefer PyPI execution, e.g. `uvx --from harnessops hops <command>`.
- `hops update-harness` should propagate that guidance into linked downstream repositories without requiring local manual edits.

## Notes

This came up because downstream `paperops` was updated to use the PyPI install path rather than a local editable HarnessOps checkout.

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。
