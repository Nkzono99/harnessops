---
name: hops-route-feedback
description: Use when classifying HarnessOps feedback into project, target, meta, protocol, external, or private dispositions.
---

Run `hops doctor --check-overlay`, then use `hops route --record <id>`.
Project evolution belongs in `research/` or `notes/`, not `harness-feedback/`.

If one event contains both a project decision and a harness gap, split it into a
project record plus upstream/meta feedback instead of forcing one disposition.
