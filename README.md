# HarnessOps

HarnessOps is a feedback routing and improvement experiment OS for AI-assisted
harness projects.

The `hops` CLI is the authoritative state engine. Agent plugins and repo-local
bridge skills delegate state-changing operations to the CLI.

## Quick Start

```bash
hops init --profile runops-project
hops doctor --check-overlay --check-records
hops add-failure --title "Harness friction" --target runops
hops route --record F0001
hops feedback export --target runops --sanitize
```

