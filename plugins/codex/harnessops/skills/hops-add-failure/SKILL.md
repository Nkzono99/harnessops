---
name: hops-add-failure
description: Use when a project failure, harness friction, local workaround, or upstream feedback candidate should be recorded through HarnessOps.
---

Use HarnessOps. Do not manually edit harness-feedback/ or harness-lab/ structure.

1. Run `hops doctor --check-overlay`.
2. If the repository is not linked, run `hops detect` and propose `hops init --profile <id>`.
3. Collect context: what happened, why bad, desired behavior, privacy risk.
4. Run `hops add-failure --interactive` or create a draft command.
5. Run `hops route --record <id>` if disposition is unclear.
6. If upstream/meta candidate, propose `hops feedback export --target <target> --sanitize`.

Keep project evolution in `research/` or `notes/`. Do not move private research
details, raw paths, or unpublished terms into upstream feedback.
