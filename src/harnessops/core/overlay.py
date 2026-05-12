from __future__ import annotations

from pathlib import Path
from typing import Any

from harnessops import __version__
from harnessops.core.lock import build_lock, load_lock, sha256_file, sha256_text, write_lock
from harnessops.core.manifest import write_manifest
from harnessops.core.project import write_project
from harnessops.profiles.registry import profile_fingerprint as registry_profile_fingerprint


class UnsafeOverwrite(RuntimeError):
    pass


FEEDBACK_README = """# harness-feedback

このディレクトリは、このプロジェクトから上流ハーネスおよび HarnessOps へのフィードバックを保存します。

このディレクトリに置くもの:

- 観測されたハーネス失敗
- disposition と期限を持つローカル回避策
- 上流フィードバック下書き
- メタハーネスフィードバック下書き

このディレクトリに置かないもの:

- 研究アジェンダ変更
- 論文主張の変更
- 実験方針転換
- 生の非公開データ
- ターゲットハーネスへの実装パッチ

レコード管理には `hops add-failure`、`hops route`、`hops feedback export --sanitize` を使います。
"""


LAB_README = """# harness-lab

このディレクトリは、このハーネスリポジトリ向けの上流改善実験を保存します。

このディレクトリに置くもの:

- インポート済みのサニタイズ済みフィードバック
- 評価ケース
- メカニズムと中止基準を持つ改善仮説
- 実験と評価スコアカード
- 証拠を伴う採用/却下判断
- メタ改善調査の構造化 research scan
- 一定サイズを超えた lab から圧縮した mutable knowledge layer

GitHub Issues は引き続きタスクトラッカーです。`harness-lab/` は評価と判断の記憶です。

採用済み判断には、証拠、回帰リスク、回帰ガードを明記する必要があります。
`hops lab compact` は正本レコードを残したまま `knowledge/lab-memory.yml` と `.md` を更新します。
"""


GENERATED_MARKER = "<!-- harnessops により生成; source records が正本 -->\n"


def default_overlay_path(mode: str) -> str:
    return "harness-feedback" if mode in {"feedback-source", "local-and-feedback"} else "harness-lab"


def default_mode(profile_id: str, profile: dict[str, Any]) -> str:
    if profile.get("mode"):
        return str(profile["mode"])
    if profile_id.endswith("-project"):
        return "feedback-source"
    if profile_id.endswith("-upstream"):
        return "upstream-lab"
    if profile_id == "harnessops-core":
        return "meta-lab"
    return "feedback-source"


def repository_kind_for_mode(mode: str) -> str:
    if mode in {"upstream-lab"}:
        return "target-repository"
    if mode == "meta-lab":
        return "harnessops-repository"
    return "project-repository"


def _write_generated(path: Path, text: str, *, force: bool, old_hash: str | None) -> None:
    if path.exists():
        current_hash = sha256_file(path)
        if path.read_text(encoding="utf-8") == text:
            return
        if not force:
            raise UnsafeOverwrite(f"既存の生成ファイルの上書きを拒否します: {path}")
        if old_hash and current_hash != old_hash:
            conflict = path.with_name(path.name + ".new")
            conflict.write_text(text, encoding="utf-8", newline="\n")
            raise UnsafeOverwrite(f"管理対象ファイルが変更されています。競合コピーを書きました: {conflict}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


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


def _touch_gitkeep(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    gitkeep = path / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")


def overlay_dirs(overlay_mode: str) -> list[str]:
    if overlay_mode in {"feedback-source", "local-and-feedback"}:
        return [
            "records/failures",
            "records/local-workarounds",
            "records/upstream-feedback",
            "records/meta-feedback",
            "views",
            "views/exported-feedback",
        ]
    return [
        "records/feedback",
        "records/eval-cases",
        "records/eval-cases/fixtures",
        "records/hypotheses",
        "records/experiments",
        "records/decisions",
        "records/research-scans",
        "improvements",
        "knowledge",
        "views",
    ]


def generated_overlay_files(overlay_mode: str, overlay_rel: str) -> dict[str, str]:
    if overlay_mode in {"feedback-source", "local-and-feedback"}:
        return {
            f"{overlay_rel}/README.md": FEEDBACK_README,
            f"{overlay_rel}/views/upstream-feedback.md": GENERATED_MARKER + "# 上流フィードバック\n\n上流フィードバックレコードはまだありません。\n",
            f"{overlay_rel}/views/open-routing.md": GENERATED_MARKER + "# 未完了ルーティング\n\n未完了のルーティングレコードはまだありません。\n",
            f"{overlay_rel}/views/exported-feedback.md": GENERATED_MARKER + "# エクスポート済みフィードバック\n\nエクスポート済みフィードバックバンドルはまだありません。\n",
        }
    return {
        f"{overlay_rel}/README.md": LAB_README,
        f"{overlay_rel}/views/imported-feedback.md": GENERATED_MARKER + "# インポート済みフィードバック\n\nインポート済みフィードバックレコードはまだありません。\n",
        f"{overlay_rel}/views/backlog.md": GENERATED_MARKER + "# バックログ\n\n評価ケースのない受理済みフィードバックはありません。\n",
        f"{overlay_rel}/views/improvements.md": GENERATED_MARKER + "# 改善dossier\n\n改善dossierはまだありません。\n",
        f"{overlay_rel}/views/research-scans.md": GENERATED_MARKER + "# Research scans\n\nresearch scan はまだありません。\n",
        f"{overlay_rel}/views/score-trajectory.md": GENERATED_MARKER + "# スコア推移\n\nスコア履歴はまだありません。\n",
    }


def refresh_managed_files(
    root: Path,
    overlay_mode: str,
    overlay_rel: str,
    *,
    force: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    old_lock = load_lock(root)
    old_managed = old_lock.get("managed_files", {}) if isinstance(old_lock.get("managed_files"), dict) else {}
    managed = dict(old_managed)
    updated: list[str] = []
    written_new: list[dict[str, str]] = []
    unchanged: list[str] = []
    overlay_root = root / overlay_rel
    if not dry_run:
        for rel in overlay_dirs(overlay_mode):
            _touch_gitkeep(overlay_root / rel)
    for rel, text in generated_overlay_files(overlay_mode, overlay_rel).items():
        path = root / rel
        template_hash = sha256_text(text)
        old_hash = old_managed.get(rel)
        if not path.exists():
            if not dry_run:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8", newline="\n")
                managed[rel] = sha256_file(path)
            updated.append(rel)
            continue
        current_hash = sha256_file(path)
        if path.read_text(encoding="utf-8") == text:
            managed[rel] = current_hash
            unchanged.append(rel)
            continue
        if force or (old_hash is not None and current_hash == old_hash):
            if not dry_run:
                path.write_text(text, encoding="utf-8", newline="\n")
                managed[rel] = sha256_file(path)
            else:
                managed[rel] = template_hash
            updated.append(rel)
        else:
            conflict = _conflict_path(path, text)
            if not dry_run:
                conflict.write_text(text, encoding="utf-8", newline="\n")
            written_new.append({"path": rel, "new": conflict.relative_to(root).as_posix()})
    if not dry_run:
        old_lock.setdefault("schema_version", "0.1")
        old_lock.setdefault("layout_version", "0.1")
        old_lock["harnessops_version"] = __version__
        old_lock["overlay"] = {"mode": overlay_mode, "path": overlay_rel}
        old_lock.setdefault("migrations", [])
        old_lock["managed_files"] = managed
        write_lock(root, old_lock)
    return {"updated": updated, "written_new": written_new, "unchanged": unchanged, "managed_files": managed}


def init_overlay(
    root: Path,
    profile: dict[str, Any],
    *,
    mode: str | None = None,
    overlay_path: str | None = None,
    with_agent_bridge: bool = False,
    dry_run: bool = False,
    force: bool = False,
) -> dict[str, Any]:
    profile_id = profile["id"]
    overlay_mode = mode or default_mode(profile_id, profile)
    overlay_rel = overlay_path or str(profile.get("feedback", {}).get("path") or default_overlay_path(overlay_mode))
    old_lock = load_lock(root)
    old_managed = old_lock.get("managed_files", {}) if isinstance(old_lock.get("managed_files"), dict) else {}
    if dry_run:
        return {
            "profile": profile_id,
            "mode": overlay_mode,
            "path": overlay_rel,
            "planned": [".harness/manifest.toml", ".harnessops/project.toml", ".harnessops/lock.json", overlay_rel],
        }

    write_manifest(root, profile, force=force)
    _touch_gitkeep(root / ".harnessops" / "migrations")
    _touch_gitkeep(root / ".harnessops" / "cache")

    project_data = {
        "schema_version": "0.1",
        "layout_version": "0.1",
        "project": {"name": root.name, "root": ".", "kind": repository_kind_for_mode(overlay_mode)},
        "profile": {
            "id": profile_id,
            "version": str(profile.get("version", "0.1.0")),
            "source": str(profile.get("source", "builtin")),
            "adapter": str(profile.get("adapter", "generic_code")),
        },
        "overlay": {"mode": overlay_mode, "path": overlay_rel, "managed_by": "harnessops"},
        "privacy": {"default_visibility": "private-until-sanitized"},
        "agents": {"codex": True, "claude": True},
    }
    target_provider = profile.get("provider")
    if target_provider:
        project_data["target_harness"] = {"provider": target_provider, "manifest": ".harness/manifest.toml"}
    write_project(root, project_data)

    managed: dict[str, str] = {}
    overlay_root = root / overlay_rel
    for rel in overlay_dirs(overlay_mode):
        _touch_gitkeep(overlay_root / rel)
    files = generated_overlay_files(overlay_mode, overlay_rel)
    for rel, text in files.items():
        path = root / rel
        _write_generated(path, text, force=force, old_hash=old_managed.get(rel))
        managed[rel] = sha256_file(path)

    bridge_managed: dict[str, str] | None = None
    if with_agent_bridge:
        from harnessops.core.agent_bridge import refresh_bridge_files

        bridge_result = refresh_bridge_files(root, codex=True, claude=False, force=force, update_lock=False)
        bridge_managed = bridge_result["managed_files"]

    lock = build_lock(
        harnessops_version=__version__,
        profile=profile,
        profile_fingerprint=registry_profile_fingerprint(profile),
        overlay_mode=overlay_mode,
        overlay_path=overlay_rel,
        managed_files=managed,
    )
    if bridge_managed is not None:
        lock["agent_bridge"] = {"managed_files": bridge_managed}
    write_lock(root, lock)
    return {"profile": profile_id, "mode": overlay_mode, "path": overlay_rel, "managed_files": managed}
