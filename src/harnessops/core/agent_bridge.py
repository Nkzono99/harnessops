from __future__ import annotations

from pathlib import Path


BRIDGE_TEXT = """---
name: harnessops-bridge
description: Use when recording project failures, routing upstream feedback, or running HarnessOps improvement workflows.
---

This repository is linked to HarnessOps.

Do not directly restructure `.harnessops/`, `harness-feedback/`, or `harness-lab/`.
Use the CLI:

- `hops doctor`
- `hops add-failure`
- `hops route`
- `hops feedback export`
- `hops feedback import`
- `hops migrate --check`

Read `.harnessops/project.toml` before proposing harness feedback or lab changes.
"""


def write_bridge(root: Path, *, codex: bool = True, claude: bool = False, force: bool = False) -> list[Path]:
    paths: list[Path] = []
    if codex:
        paths.append(root / ".agents" / "skills" / "harnessops-bridge" / "SKILL.md")
    if claude:
        paths.append(root / ".claude" / "skills" / "harnessops-bridge" / "SKILL.md")
    for path in paths:
        if path.exists() and not force:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(BRIDGE_TEXT, encoding="utf-8")
    return paths

