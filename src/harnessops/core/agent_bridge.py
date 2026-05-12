from __future__ import annotations

from pathlib import Path


BRIDGE_TEXT = """---
name: harnessops-bridge
description: プロジェクト失敗の記録、上流フィードバックのルーティング、HarnessOps 改善ワークフローの実行時に使う。
---

このリポジトリは HarnessOps にリンクされています。

ハーネス状態の正本は `hops` CLI です。まず `.harnessops/project.toml` を読み、profile、overlay mode、overlay path を確認してください。
PATH に `hops` がない環境では `uv run --with-editable . hops <command>` を使います。

`.harnessops/`、`harness-feedback/`、`harness-lab/` の構造を直接組み替えないでください。レコード作成、ルーティング、エクスポート/インポート、ラボ評価、採用判断は CLI に委譲します。

- `hops doctor --check-overlay`
- `hops add-failure`
- `hops route`
- `hops add-feedback`
- `hops feedback export --sanitize`
- `hops feedback import <bundle-path>`
- `hops lab new-eval-case --from <FBid>`
- `hops propose --from <Eid>`
- `hops eval --case <Eid> --manual`
- `hops decide --from <id> --status <status>`
- `hops migrate --check`

外部共有前にサニタイズ済みバンドルを確認し、ローカルパス、非公開語、未公開研究の文脈を残さないでください。
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
