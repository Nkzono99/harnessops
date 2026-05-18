---
name: hops-global-share-state
description: global/local-state HarnessOps の状態を repo を汚さず zip 化、取り込み、または現在の local state へ merge するときに使う。
---

Use `uvx --from harnessops hops <command>`; do not rely on `hops` being on PATH.

This skill is for sharing local HarnessOps state between people or machines without committing `.harnessops/`, `harness-feedback/`, `harness-lab/`, or `.agents/skills/` to the target repository.

## Resolve First

Start from the current repository and resolve the HarnessOps project.

```bash
uvx --from harnessops hops project resolve --json
```

If it is not linked and the user wants global/local-state usage, detect and link locally.

```bash
uvx --from harnessops hops detect --json
uvx --from harnessops hops project link --storage local --profile <profile-id>
```

Then validate before packing or merging.

```bash
uvx --from harnessops hops doctor --check-overlay --check-records
```

## Pack For Sharing

Use this when the user asks to bundle, hand off, back up, or share their local HarnessOps state.

```bash
uvx --from harnessops hops local pack
```

Without `--output`, the CLI writes under the user's HarnessOps home exports directory, not the target repository. Use `--output <path>.zip` only when the user requests a specific destination.

## Import A Pack As A Separate Project

Use this when the user receives a bundle and wants to register it as its own global project entry.

```bash
uvx --from harnessops hops local import <path>.zip
```

Add `--force` only when the user explicitly accepts replacing an existing imported project id.

## Merge Into The Current Local Project

Use this when the user wants another bundle or state directory merged into the currently resolved local-state project.

```bash
uvx --from harnessops hops local merge <path-or-state-dir>
```

After merging, validate again:

```bash
uvx --from harnessops hops doctor --check-overlay --check-records
```

## Rules

- Do not create repo-local HarnessOps files for sharing unless the user explicitly asks to switch away from global/local-state.
- Do not unzip or hand-edit local state directories as the normal path; pack/import/merge through `hops local`.
- Do not share raw bundles externally if they contain private context. For public upstream feedback, use `hops feedback export --sanitize` or `hops-global-feedback-issue` instead.
- Report the resulting bundle path, imported state root, or merged record count from CLI output.
