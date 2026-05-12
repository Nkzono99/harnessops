---
name: hops-route-feedback
description: Use when classifying HarnessOps feedback into project, target, meta, protocol, external, or private dispositions.
---

Run `hops route --record <id>` after `hops doctor --check-overlay`.

If one event contains both project evolution and a harness gap, split it into
separate records. Do not upstream project-specific context.
