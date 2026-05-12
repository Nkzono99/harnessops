from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer

from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.records import create_imported_feedback, next_id, read_record
from harnessops.core.render import refresh_views
from harnessops.core.sanitize import sanitize_text
from harnessops.profiles.registry import load_profile

feedback_app = typer.Typer(help="フィードバックバンドルをエクスポート/インポートします。")


@feedback_app.command("export")
def export_feedback(
    target: Optional[str] = typer.Option(None, "--target"),
    sanitize: bool = typer.Option(False, "--sanitize"),
    format: str = typer.Option("markdown", "--format"),  # noqa: A002
    allow_private: bool = typer.Option(False, "--allow-private"),
) -> None:
    """プロジェクト側レコードからサニタイズ済み上流/メタフィードバックバンドルを生成します。"""
    root = find_root()
    project = load_project(root)
    if not sanitize and not allow_private:
        typer.echo("--allow-private なしの未サニタイズエクスポートは拒否します")
        raise typer.Exit(1)
    profile = load_profile(project.profile_id)
    records = []
    target_filter = target or "all"
    for path in sorted((project.overlay_dir / "records/failures").glob("*.md")):
        frontmatter, body = read_record(path)
        disposition = frontmatter.get("disposition", {})
        if disposition.get("type") not in {"target-upstream-candidate", "meta-harness-candidate", "protocol-candidate"}:
            continue
        if disposition.get("target") == target_filter or target_filter == "all":
            records.append((path, frontmatter, body))
    for rel in ["records/upstream-feedback", "records/meta-feedback"]:
        for path in sorted((project.overlay_dir / rel).glob("*.md")):
            frontmatter, body = read_record(path)
            if frontmatter.get("target") == target_filter or target_filter == "all":
                records.append((path, frontmatter, body))
    if not records:
        typer.echo("一致するフィードバックレコードがありません")
        raise typer.Exit(1)
    resolved_targets = sorted({str(record[1].get("target") or record[1].get("disposition", {}).get("target") or "unknown") for record in records})
    export_target = target or ("mixed" if len(resolved_targets) != 1 else resolved_targets[0])
    prefix = "MF" if export_target == "harnessops" else "UF"
    out_dir = project.overlay_dir / "views" / "exported-feedback"
    out_dir.mkdir(parents=True, exist_ok=True)
    export_id = next_id(out_dir, prefix)
    title = f"{export_target} へのフィードバック"
    sections = []
    for path, frontmatter, body in records:
        sections.append(f"## 送信元 {frontmatter.get('id')}: {path.name}\n\n{body.strip()}\n")
    bundle_body = "\n".join(sections)
    if sanitize:
        bundle_body = sanitize_text(bundle_body, root=root, profile=profile, allow_private=allow_private)
    if format in {"issue", "github-issue"}:
        bundle_body = "## Issue下書き\n\n" + bundle_body + "\n\n## 確認\n\nこれは下書きのみです。HarnessOps はリモートIssueを自動作成しません。\n"
    frontmatter = {
        "id": export_id,
        "record_type": "meta_feedback" if prefix == "MF" else "upstream_feedback",
        "created_at": records[0][1].get("created_at"),
        "status": "draft",
        "target": export_target,
        "source_failure": records[0][1].get("id"),
        "sanitized": bool(sanitize),
        "visibility": "sanitized" if sanitize else "private-until-sanitized",
        "format": format,
        "included_targets": resolved_targets,
    }
    text = "---\n" + json.dumps(frontmatter, indent=2) + "\n---\n\n# " + title + "\n\n" + bundle_body
    out_path = out_dir / f"{export_id}-{export_target}-feedback.md"
    out_path.write_text(text, encoding="utf-8")
    refresh_views(root, project.overlay_path)
    typer.echo(out_path.relative_to(root).as_posix())


@feedback_app.command("import")
def import_feedback(
    path: Optional[Path] = typer.Argument(None),
    issue: Optional[int] = typer.Option(None, "--issue"),
    repo: Optional[str] = typer.Option(None, "--repo"),
) -> None:
    """フィードバックバンドルをターゲット側 harness-lab にインポートします。"""
    root = find_root()
    project = load_project(root)
    if project.overlay_mode not in {"upstream-lab", "meta-lab"}:
        typer.echo("feedback import には upstream-lab または meta-lab mode が必要です")
        raise typer.Exit(1)
    if issue is not None:
        source = {"id": f"ISSUE-{issue}", "record_type": "upstream_feedback", "issue": {"url": f"https://github.com/{repo or 'unknown'}/issues/{issue}"}}
        body = f"{repo or 'unknown'} から GitHub issue {issue} をインポートしました。"
        title = f"GitHub issue {issue}"
    elif path is not None:
        source_path = path if path.is_absolute() else root / path
        source, body = read_record(source_path)
        if source.get("record_type") not in {"upstream_feedback", "meta_feedback"} or not source.get("sanitized", False):
            typer.echo("import にはサニタイズ済み upstream_feedback または meta_feedback バンドルが必要です")
            raise typer.Exit(1)
        title = source_path.stem
    else:
        typer.echo("バンドルパスまたは --issue を指定してください")
        raise typer.Exit(1)
    out_path = create_imported_feedback(project, source_record=source, body=body, title=title)
    refresh_views(root, project.overlay_path)
    typer.echo(out_path.relative_to(root).as_posix())


def register(app: typer.Typer) -> None:
    app.add_typer(feedback_app, name="feedback")
