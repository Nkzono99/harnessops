from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Any

from harnessops.core.lock import load_lock, sha256_file, write_lock

BRIDGE_TEXT = """---
name: harnessops-bridge
description: プロジェクト失敗の記録、上流フィードバックのルーティング、HarnessOps 改善ワークフローの実行時に使う。
---

このリポジトリは HarnessOps にリンクされています。

ハーネス状態の正本は `hops` CLI です。まず `.harnessops/project.toml` を読み、profile、overlay mode、overlay path を確認してください。
下流の target/project repo では PATH 上の `hops` に依存せず、原則 `uvx --from harnessops hops <command>` を使います。

`.harnessops/`、`harness-feedback/`、`harness-lab/` の構造を直接組み替えないでください。レコード作成、ルーティング、エクスポート/インポート、ラボ評価、採用判断は CLI に委譲します。

- `uvx --from harnessops hops doctor --check-overlay`
- `uvx --from harnessops hops add-failure`
- `uvx --from harnessops hops route`
- `uvx --from harnessops hops add-feedback`
- `uvx --from harnessops hops feedback export --sanitize`
- `uvx --from harnessops hops feedback import <bundle-path>`
- `uvx --from harnessops hops lab capture --title <title> --summary <summary> --expected-change <expected>`
- `uvx --from harnessops hops lab dossier --from <FBid>`
- `uvx --from harnessops hops lab investigate --from <IMPid> --summary <summary>`
- `uvx --from harnessops hops lab classify --from <IMPid>`
- `uvx --from harnessops hops lab new-eval-case --from <FBid>`
- `uvx --from harnessops hops propose --from <Eid>`
- `uvx --from harnessops hops eval --case <Eid> --manual`
- `uvx --from harnessops hops decide --from <id> --status <status>`
- `uvx --refresh-package harnessops --from harnessops hops update-harness`
- `uvx --from harnessops hops migrate --check`

外部共有前にサニタイズ済みバンドルを確認し、ローカルパス、非公開語、未公開研究の文脈を残さないでください。
"""


def packaged_plugin_source(host: str) -> Path:
    source_root = Path(__file__).resolve().parents[3] / "plugins" / host / "harnessops"
    if source_root.exists():
        return source_root
    return Path(str(resources.files("harnessops").joinpath("agent_assets", "plugins", host, "harnessops")))


def _conflict_path(path: Path, text: str) -> Path:
    candidate = path.with_name(path.name + ".new")
    if not candidate.exists() or candidate.read_text(encoding="utf-8") == text:
        return candidate
    index = 1
    while True:
        numbered = path.with_name(f"{path.name}.new.{index}")
        if not numbered.exists() or numbered.read_text(encoding="utf-8") == text:
            return numbered
        index += 1


def _packaged_skill_files(source: Path, destination: Path) -> dict[Path, str]:
    skills_dir = source / "skills"
    if not skills_dir.exists():
        raise FileNotFoundError(f"HarnessOps skill assets not found: {skills_dir}")
    files: dict[Path, str] = {}
    for skill_dir in sorted(path for path in skills_dir.iterdir() if (path / "SKILL.md").exists()):
        for source_file in sorted(path for path in skill_dir.rglob("*") if path.is_file()):
            target = destination / source_file.relative_to(skills_dir)
            files[target] = source_file.read_text(encoding="utf-8")
    return files


def packaged_bridge_files(root: Path, *, codex: bool = True, claude: bool = False) -> dict[Path, str]:
    files: dict[Path, str] = {}
    if codex:
        files[root / ".agents" / "skills" / "harnessops-bridge" / "SKILL.md"] = BRIDGE_TEXT
        files.update(_packaged_skill_files(packaged_plugin_source("codex"), root / ".agents" / "skills"))
    if claude:
        files[root / ".claude" / "skills" / "harnessops-bridge" / "SKILL.md"] = BRIDGE_TEXT
        files.update(_packaged_skill_files(packaged_plugin_source("claude"), root / ".claude" / "skills"))
    return files


def refresh_bridge_files(
    root: Path,
    *,
    codex: bool = True,
    claude: bool = False,
    force: bool = False,
    dry_run: bool = False,
    update_lock: bool = True,
) -> dict[str, Any]:
    lock = load_lock(root)
    bridge_lock = lock.get("agent_bridge", {}) if isinstance(lock.get("agent_bridge"), dict) else {}
    old_managed = (
        bridge_lock.get("managed_files", {})
        if isinstance(bridge_lock.get("managed_files"), dict)
        else {}
    )
    managed = dict(old_managed)
    checked: list[str] = []
    updated: list[str] = []
    unchanged: list[str] = []
    conflicted: list[str] = []
    written_new: list[dict[str, str]] = []

    for path, text in packaged_bridge_files(root, codex=codex, claude=claude).items():
        rel = path.relative_to(root).as_posix()
        checked.append(rel)
        old_hash = old_managed.get(rel)
        if not path.exists():
            if not dry_run:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8", newline="\n")
                managed[rel] = sha256_file(path)
            updated.append(rel)
            continue

        current_text = path.read_text(encoding="utf-8")
        current_hash = sha256_file(path)
        if current_text == text:
            managed[rel] = current_hash
            unchanged.append(rel)
            continue

        if force or (old_hash is not None and current_hash == old_hash):
            if not dry_run:
                path.write_text(text, encoding="utf-8", newline="\n")
                managed[rel] = sha256_file(path)
            updated.append(rel)
            continue

        conflict = _conflict_path(path, text)
        if not dry_run:
            conflict.write_text(text, encoding="utf-8", newline="\n")
        conflicted.append(rel)
        written_new.append({"path": rel, "new": conflict.relative_to(root).as_posix()})

    if update_lock and not dry_run:
        lock["agent_bridge"] = {"managed_files": managed}
        write_lock(root, lock)

    return {
        "checked": checked,
        "updated": updated,
        "unchanged": unchanged,
        "conflicted": conflicted,
        "written_new": written_new,
        "managed_files": managed,
    }


def write_bridge(root: Path, *, codex: bool = True, claude: bool = False, force: bool = False) -> list[Path]:
    result = refresh_bridge_files(
        root,
        codex=codex,
        claude=claude,
        force=force,
        update_lock=False,
    )
    return [root / rel for rel in result["checked"]]
