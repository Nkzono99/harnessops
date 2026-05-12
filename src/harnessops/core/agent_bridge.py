from __future__ import annotations

from pathlib import Path


BRIDGE_TEXT = """---
name: harnessops-bridge
description: プロジェクト失敗の記録、上流フィードバックのルーティング、HarnessOps 改善ワークフローの実行時に使う。
---

このリポジトリは HarnessOps にリンクされています。

`.harnessops/`、`harness-feedback/`、`harness-lab/` を直接組み替えないでください。
CLI を使います。

- `hops doctor`
- `hops add-failure`
- `hops route`
- `hops feedback export`
- `hops feedback import`
- `hops migrate --check`

ハーネスフィードバックやラボ変更を提案する前に `.harnessops/project.toml` を読んでください。
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
