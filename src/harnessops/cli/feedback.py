from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Optional

import typer

from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.records import create_imported_feedback, next_id, read_record
from harnessops.core.render import refresh_views
from harnessops.core.sanitize import sanitize_text
from harnessops.profiles.registry import load_profile

feedback_app = typer.Typer(help="フィードバックバンドルをエクスポート/インポートします。")


def _placeholder_issue_source(issue: int, repo: str | None) -> tuple[dict[str, Any], str, str]:
    source = {
        "id": f"ISSUE-{issue}",
        "record_type": "upstream_feedback",
        "issue": {
            "provider": "github",
            "repo": repo or "unknown",
            "number": issue,
            "url": f"https://github.com/{repo or 'unknown'}/issues/{issue}",
        },
    }
    body = f"{repo or 'unknown'} から GitHub issue {issue} をインポートしました。"
    return source, body, f"GitHub issue {issue}"


def _issue_label_names(labels: object) -> list[str]:
    if not isinstance(labels, list):
        return []
    names: list[str] = []
    for label in labels:
        if isinstance(label, dict) and label.get("name"):
            names.append(str(label["name"]))
    return names


def _issue_author_login(value: object) -> str | None:
    if isinstance(value, dict) and value.get("login"):
        return str(value["login"])
    return None


def _issue_comments(value: object) -> list[dict[str, str | None]]:
    if not isinstance(value, list):
        return []
    comments: list[dict[str, str | None]] = []
    for comment in value:
        if not isinstance(comment, dict):
            continue
        comments.append(
            {
                "author": _issue_author_login(comment.get("author")),
                "created_at": str(comment.get("createdAt")) if comment.get("createdAt") else None,
                "body": str(comment.get("body") or ""),
            }
        )
    return comments


def _load_github_issue(issue: int, repo: str | None) -> tuple[dict[str, Any], str, str]:
    source, fallback_body, fallback_title = _placeholder_issue_source(issue, repo)
    if not repo:
        return source, fallback_body, fallback_title
    try:
        result = subprocess.run(
            [
                "gh",
                "issue",
                "view",
                str(issue),
                "--repo",
                repo,
                "--json",
                "number,title,body,author,labels,createdAt,updatedAt,url,comments",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
    except (FileNotFoundError, json.JSONDecodeError, subprocess.CalledProcessError):
        return source, fallback_body, fallback_title

    issue_labels = _issue_label_names(payload.get("labels"))
    issue_comments = _issue_comments(payload.get("comments"))
    issue_data: dict[str, Any] = {
        "provider": "github",
        "repo": repo,
        "number": int(payload.get("number") or issue),
        "url": str(payload.get("url") or f"https://github.com/{repo}/issues/{issue}"),
        "title": str(payload.get("title") or fallback_title),
        "author": _issue_author_login(payload.get("author")),
        "labels": issue_labels,
        "created_at": str(payload.get("createdAt")) if payload.get("createdAt") else None,
        "updated_at": str(payload.get("updatedAt")) if payload.get("updatedAt") else None,
        "comments": issue_comments,
    }
    source = {
        "id": f"ISSUE-{issue_data['number']}",
        "record_type": "upstream_feedback",
        "issue": issue_data,
    }
    labels = ", ".join(issue_labels) or "なし"
    body_parts = [
        f"GitHub issue: {issue_data['url']}",
        f"author: {issue_data['author'] or 'unknown'}",
        f"labels: {labels}",
        f"created_at: {issue_data['created_at'] or 'unknown'}",
        f"updated_at: {issue_data['updated_at'] or 'unknown'}",
        "",
        "## Issue本文",
        str(payload.get("body") or "本文はありません。").strip(),
    ]
    if issue_comments:
        body_parts.extend(["", "## コメント"])
        for index, comment in enumerate(issue_comments, start=1):
            body_parts.extend(
                [
                    f"### Comment {index}: {comment.get('author') or 'unknown'}",
                    comment.get("body") or "",
                ]
            )
    return source, "\n".join(body_parts).strip(), str(issue_data["title"])


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
        source, body, title = _load_github_issue(issue, repo)
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
