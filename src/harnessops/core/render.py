from __future__ import annotations

from pathlib import Path

from harnessops.core.lock import load_lock, sha256_file, write_lock
from harnessops.core.overlay import GENERATED_MARKER
from harnessops.core.records import read_record


def _refresh_managed_hashes(root: Path, written: list[Path]) -> None:
    lock = load_lock(root)
    managed = lock.get("managed_files")
    if not isinstance(managed, dict):
        return
    changed = False
    for path in written:
        rel = path.relative_to(root).as_posix()
        if rel in managed or path.read_text(encoding="utf-8").startswith(GENERATED_MARKER):
            managed[rel] = sha256_file(path)
            changed = True
    if changed:
        lock["managed_files"] = managed
        write_lock(root, lock)


def refresh_views(root: Path, overlay_rel: str) -> list[Path]:
    overlay = root / overlay_rel
    written: list[Path] = []
    if overlay.name == "harness-feedback":
        failures = []
        for path in sorted((overlay / "records/failures").glob("*.md")):
            frontmatter, _ = read_record(path)
            disposition = frontmatter.get("disposition", {})
            failures.append(
                f"- `{frontmatter.get('id')}` "
                f"{disposition.get('type')} -> {disposition.get('target')}\n"
            )
        view = overlay / "views" / "open-routing.md"
        view.write_text(
            GENERATED_MARKER
            + "# 未完了ルーティング\n\n"
            + ("".join(failures) or "失敗レコードはまだありません。\n"),
            encoding="utf-8",
            newline="\n",
        )
        written.append(view)
    else:
        rows = []
        for path in sorted((overlay / "records/feedback").glob("*.md")):
            frontmatter, _ = read_record(path)
            classification = frontmatter.get("classification", {})
            rows.append(
                f"- `{frontmatter.get('id')}` {frontmatter.get('status')} "
                f"{classification.get('capability')} {classification.get('failure_class')}\n"
            )
        view = overlay / "views" / "imported-feedback.md"
        view.write_text(
            GENERATED_MARKER
            + "# インポート済みフィードバック\n\n"
            + ("".join(rows) or "インポート済みフィードバックレコードはまだありません。\n"),
            encoding="utf-8",
            newline="\n",
        )
        written.append(view)
        improvement_rows = []
        for path in sorted((overlay / "improvements").glob("IMP*.md")):
            frontmatter, _ = read_record(path)
            classification = frontmatter.get("classification", {})
            improvement_rows.append(
                f"- `{frontmatter.get('id')}` {frontmatter.get('status')} "
                f"maturity={frontmatter.get('maturity', 'raw')} "
                f"scope={frontmatter.get('scope', 'unknown')} "
                f"promotion={frontmatter.get('promotion_level', 'unknown')} "
                f"source={frontmatter.get('source_feedback')} "
                f"{classification.get('capability')} {classification.get('failure_class')}\n"
            )
        improvements_view = overlay / "views" / "improvements.md"
        improvements_view.write_text(
            GENERATED_MARKER
            + "# 改善dossier\n\n"
            + ("".join(improvement_rows) or "改善dossierはまだありません。\n"),
            encoding="utf-8",
            newline="\n",
        )
        written.append(improvements_view)
    _refresh_managed_hashes(root, written)
    return written
