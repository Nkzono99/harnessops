from __future__ import annotations

import shutil
from importlib import resources
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
- `hops update-harness`
- `hops migrate --check`

外部共有前にサニタイズ済みバンドルを確認し、ローカルパス、非公開語、未公開研究の文脈を残さないでください。
"""


def packaged_plugin_source(host: str) -> Path:
    source_root = Path(__file__).resolve().parents[3] / "plugins" / host / "harnessops"
    if source_root.exists():
        return source_root
    return Path(str(resources.files("harnessops").joinpath("agent_assets", "plugins", host, "harnessops")))


def _copy_skill_dirs(source: Path, destination: Path, *, force: bool) -> list[Path]:
    written: list[Path] = []
    skills_dir = source / "skills"
    if not skills_dir.exists():
        raise FileNotFoundError(f"HarnessOps skill assets not found: {skills_dir}")
    for skill_dir in sorted(path for path in skills_dir.iterdir() if (path / "SKILL.md").exists()):
        target = destination / skill_dir.name
        if target.exists():
            if not force:
                written.append(target / "SKILL.md")
                continue
            shutil.rmtree(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(skill_dir, target)
        written.append(target / "SKILL.md")
    return written


def write_bridge(root: Path, *, codex: bool = True, claude: bool = False, force: bool = False) -> list[Path]:
    paths: list[Path] = []
    if codex:
        paths.append(root / ".agents" / "skills" / "harnessops-bridge" / "SKILL.md")
        paths.extend(_copy_skill_dirs(packaged_plugin_source("codex"), root / ".agents" / "skills", force=force))
    if claude:
        paths.append(root / ".claude" / "skills" / "harnessops-bridge" / "SKILL.md")
        paths.extend(_copy_skill_dirs(packaged_plugin_source("claude"), root / ".claude" / "skills", force=force))
    for path in paths:
        if path.exists() and not force:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.parent.name == "harnessops-bridge":
            path.write_text(BRIDGE_TEXT, encoding="utf-8")
    return paths
