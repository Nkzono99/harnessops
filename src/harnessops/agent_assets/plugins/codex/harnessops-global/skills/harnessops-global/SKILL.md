---
name: harnessops-global
description: Use HarnessOps from Codex through the user's global registry and local state, without requiring .harnessops, harness-feedback, harness-lab, or repo-local skills in the target repository.
---

HarnessOps state changes are owned by the `hops` CLI. In ordinary target/project repositories, do not assume `hops` is on `PATH`; invoke it as:

```bash
uvx --from harnessops hops <command>
```

## Skill-First Workflow

Use this skill as the normal entry point for global/local-state HarnessOps work. The user should be able to ask in ordinary language, and the agent should translate that request into `uvx --from harnessops hops ...` commands.

Intent mapping:

| User intent | Agent action |
|---|---|
| "Use HarnessOps here" / "set this repo up locally" | Resolve, detect if needed, then `project link --storage local`. |
| "Record this failure" | Resolve/link, run doctor, then `feedback add-failure`. |
| "Classify this" | Resolve/link, then `feedback route --record <id>` or classify supplied text. |
| "Prepare this for sharing" | Use `feedback add` if needed, then `feedback export --sanitize`. |
| "Make a GitHub issue" / "issue化して" | Use `hops-global-feedback-issue`; export with `--format github-issue`, show duplicate candidates, create only with explicit confirmation. |
| "Use this feedback in a lab" | Ensure an upstream/meta profile, then `feedback import` or `lab capture`. |
| "Share my local HarnessOps state" | Use `hops-global-share-state`; pack with `local pack` or an explicit `--output <zip>`. |
| "Bring in someone else's local state" | Use `hops-global-share-state`; `local import` for a new registry entry, or `local merge` into the current project. |

If the user asks for repo-local HarnessOps files, stop using this global-only path and use repo-local commands such as `uvx --from harnessops hops init --profile <id>` or `uvx --from harnessops hops agent bridge --codex`.

## Resolve Before Action

1. Resolve the current repository first:

```bash
uvx --from harnessops hops project resolve --json
```

2. If the project is not linked, detect and create a local-state link. This writes to the user's HarnessOps home, not to the repository:

```bash
uvx --from harnessops hops detect --json
uvx --from harnessops hops project link --storage local --profile <profile-id>
```

3. Validate before making HarnessOps state changes:

```bash
uvx --from harnessops hops doctor --check-overlay --check-records
```

4. Use role-appropriate commands after resolution:

```bash
uvx --from harnessops hops feedback add-failure ...
uvx --from harnessops hops feedback route --record <id>
uvx --from harnessops hops feedback export --sanitize
uvx --from harnessops hops feedback import <bundle-path>
uvx --from harnessops hops lab capture --title <title> --summary <summary> --expected-change <expected>
uvx --from harnessops hops local pack
uvx --from harnessops hops local merge <zip-or-state-dir>
```

## Default Agent Behavior

- Prefer doing the work through this skill instead of asking the user to run CLI commands themselves.
- Use `project resolve --json` at the start of each task and trust repo-local `.harnessops/project.toml` if it exists.
- If the repo is not linked and the user has not requested repo-local files, use `project link --storage local`.
- Choose `generic-code` only when detection does not return a more specific profile and the user has not specified one.
- After any state-changing command, report the created record path or pack path in user-facing terms.
- For generated paths outside the repo, say they are in local HarnessOps state rather than asking the user to look under the target repo.

## Rules

- Keep ordinary repositories clean. Do not create `.harnessops/`, `harness-feedback/`, `harness-lab/`, or `.agents/skills/` unless the user explicitly asks for repo-local HarnessOps usage.
- If a repository already has `.harnessops/project.toml`, respect that repo-local project. Global registry is the fallback when repo-local metadata is absent.
- Do not directly reorganize HarnessOps state directories. Records, routing, import/export, lab evaluation, and merge operations go through `uvx --from harnessops hops`.
- External sharing must go through sanitize/export. Do not paste unsanitized local paths, private terms, or unpublished project context into remote issues or PRs.
