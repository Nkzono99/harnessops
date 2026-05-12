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

feedback_app = typer.Typer(help="Export and import feedback bundles.")


@feedback_app.command("export")
def export_feedback(
    target: str = typer.Option(..., "--target"),
    sanitize: bool = typer.Option(False, "--sanitize"),
    format: str = typer.Option("markdown", "--format"),  # noqa: A002
    allow_private: bool = typer.Option(False, "--allow-private"),
) -> None:
    """Generate sanitized upstream/meta feedback bundles from project-side records."""
    root = find_root()
    project = load_project(root)
    if not sanitize and not allow_private:
        typer.echo("refusing unsanitized export without --allow-private")
        raise typer.Exit(1)
    profile = load_profile(project.profile_id)
    records = []
    for path in sorted((project.overlay_dir / "records/failures").glob("*.md")):
        frontmatter, body = read_record(path)
        disposition = frontmatter.get("disposition", {})
        if disposition.get("target") == target or target == "all":
            records.append((path, frontmatter, body))
    if not records:
        typer.echo("no matching feedback records")
        raise typer.Exit(1)
    prefix = "MF" if target == "harnessops" else "UF"
    out_dir = project.overlay_dir / "views" / "exported-feedback"
    out_dir.mkdir(parents=True, exist_ok=True)
    export_id = next_id(out_dir, prefix)
    title = f"Feedback to {target}"
    sections = []
    for path, frontmatter, body in records:
        sections.append(f"## Source {frontmatter.get('id')}: {path.name}\n\n{body.strip()}\n")
    bundle_body = "\n".join(sections)
    if sanitize:
        bundle_body = sanitize_text(bundle_body, root=root, profile=profile, allow_private=allow_private)
    frontmatter = {
        "id": export_id,
        "record_type": "meta_feedback" if prefix == "MF" else "upstream_feedback",
        "created_at": records[0][1].get("created_at"),
        "status": "draft",
        "target": target,
        "source_failure": records[0][1].get("id"),
        "sanitized": bool(sanitize),
        "visibility": "sanitized" if sanitize else "private-until-sanitized",
        "format": format,
    }
    text = "---\n" + json.dumps(frontmatter, indent=2) + "\n---\n\n# " + title + "\n\n" + bundle_body
    out_path = out_dir / f"{export_id}-{target}-feedback.md"
    out_path.write_text(text, encoding="utf-8")
    refresh_views(root, project.overlay_path)
    typer.echo(out_path.relative_to(root).as_posix())


@feedback_app.command("import")
def import_feedback(
    path: Optional[Path] = typer.Argument(None),
    issue: Optional[int] = typer.Option(None, "--issue"),
    repo: Optional[str] = typer.Option(None, "--repo"),
) -> None:
    """Import a feedback bundle into target-side harness-lab."""
    root = find_root()
    project = load_project(root)
    if project.overlay_mode not in {"upstream-lab", "meta-lab"}:
        typer.echo("feedback import requires upstream-lab or meta-lab mode")
        raise typer.Exit(1)
    if issue is not None:
        source = {"id": f"ISSUE-{issue}", "record_type": "upstream_feedback", "issue": {"url": f"https://github.com/{repo or 'unknown'}/issues/{issue}"}}
        body = f"Imported GitHub issue {issue} from {repo or 'unknown'}."
        title = f"GitHub issue {issue}"
    elif path is not None:
        source_path = path if path.is_absolute() else root / path
        source, body = read_record(source_path)
        title = source_path.stem
    else:
        typer.echo("provide a bundle path or --issue")
        raise typer.Exit(1)
    out_path = create_imported_feedback(project, source_record=source, body=body, title=title)
    refresh_views(root, project.overlay_path)
    typer.echo(out_path.relative_to(root).as_posix())


def register(app: typer.Typer) -> None:
    app.add_typer(feedback_app, name="feedback")

