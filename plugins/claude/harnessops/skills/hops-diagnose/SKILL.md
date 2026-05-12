---
name: hops-diagnose
description: Use when checking whether a repository is linked to HarnessOps and whether the overlay is healthy.
---

Run `hops doctor --check-overlay`. If the repository is not linked, run `hops detect`
and propose `hops init --profile <detected-profile>`.

