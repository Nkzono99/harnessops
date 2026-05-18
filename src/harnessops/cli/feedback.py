from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Optional

import typer

from harnessops.cli.add_failure import add_failure_command, add_feedback_command
from harnessops.cli.route import route_command
from harnessops.core.issue_bridge import (
    create_github_issue,
    remaining_private_markers,
    search_duplicate_issues,
    validate_repo,
)
from harnessops.core.lab_records import create_imported_feedback
from harnessops.core.paths import find_root
from harnessops.core.project import load_project
from harnessops.core.record_index import next_id
from harnessops.core.record_io import dump_record, read_record
from harnessops.core.render import refresh_project_views
from harnessops.core.sanitize import sanitize_text
from harnessops.profiles.registry import load_profile

feedback_app = typer.Typer(
    help="フィードバックの記録、分類、エクスポート/インポートを扱います。"
)
issue_app = typer.Typer(
    help="サニタイズ済みフィードバックをGitHub Issueへ橋渡しします。"
)


def _placeholder_issue_source(
    issue: int, repo: str | None
) -> tuple[dict[str, Any], str, str]:
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
                "created_at": str(comment.get("createdAt"))
                if comment.get("createdAt")
                else None,
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
            encoding="utf-8",
            errors="replace",
        )
        payload = json.loads(result.stdout)
    except (
        FileNotFoundError,
        TypeError,
        json.JSONDecodeError,
        subprocess.CalledProcessError,
    ):
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
        "created_at": str(payload.get("createdAt"))
        if payload.get("createdAt")
        else None,
        "updated_at": str(payload.get("updatedAt"))
        if payload.get("updatedAt")
        else None,
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


def _resolve_bundle_path(root: Path, bundle: Path) -> Path:
    return bundle if bundle.is_absolute() else root / bundle


def _load_issue_bundle(
    root: Path, profile: dict[str, Any], bundle_path: Path
) -> tuple[dict[str, Any], str]:
    if not bundle_path.exists():
        typer.echo(f"バンドルが見つかりません: {bundle_path}")
        raise typer.Exit(1)
    source, body = read_record(bundle_path)
    if source.get("record_type") not in {"upstream_feedback", "meta_feedback"}:
        typer.echo(
            "GitHub Issue化には upstream_feedback または meta_feedback が必要です"
        )
        raise typer.Exit(1)
    if not source.get("sanitized", False):
        typer.echo("GitHub Issue化にはサニタイズ済みバンドルが必要です")
        raise typer.Exit(1)
    if source.get("format") not in {"issue", "github-issue"}:
        typer.echo("GitHub Issue化には --format github-issue のバンドルが必要です")
        raise typer.Exit(1)
    markers = remaining_private_markers(root, profile, body)
    if markers:
        typer.echo(
            "GitHub Issue化する前に再サニタイズが必要です: " + ", ".join(markers)
        )
        raise typer.Exit(1)
    return source, body.strip()


def _issue_title(source: dict[str, Any], body: str, override: str | None) -> str:
    if override:
        return override
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    target = source.get("target") or "feedback"
    return f"{target} feedback"


def _write_fallback_issue_draft(bundle_path: Path, title: str, body: str) -> Path:
    base = bundle_path.with_name(f"{bundle_path.stem}-github-issue-draft.md")
    candidate = base
    index = 2
    while candidate.exists():
        candidate = bundle_path.with_name(
            f"{bundle_path.stem}-github-issue-draft-{index}.md"
        )
        index += 1
    candidate.write_text(f"# {title}\n\n{body.strip()}\n", encoding="utf-8", newline="\n")
    return candidate


def _source_record_paths(
    project_root: Path,
    project_overlay: Path,
    bundle_path: Path,
    source: dict[str, Any],
) -> list[Path]:
    paths: list[Path] = []
    records_root = (project_overlay / "records").resolve()
    for rel_path in source.get("source_record_paths", []) or []:
        if not isinstance(rel_path, str):
            continue
        candidate = (project_root / rel_path).resolve()
        if candidate.exists() and candidate.is_relative_to(records_root):
            paths.append(candidate)
    for record_id in source.get("source_records", []) or []:
        if not isinstance(record_id, str):
            continue
        for candidate in sorted((project_overlay / "records").rglob("*.md")):
            frontmatter, _ = read_record(candidate)
            if frontmatter.get("id") == record_id or candidate.name.startswith(
                record_id
            ):
                paths.append(candidate)
                break
    try:
        if bundle_path.is_relative_to(project_overlay / "records"):
            paths.append(bundle_path)
    except ValueError:
        pass
    unique_paths: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            unique_paths.append(path)
            seen.add(resolved)
    return unique_paths


def _write_issue_url_to_records(
    root: Path,
    bundle_path: Path,
    source: dict[str, Any],
    *,
    repo: str,
    url: str,
) -> int:
    project = load_project(root)
    updated = 0
    for path in _source_record_paths(root, project.overlay_dir, bundle_path, source):
        frontmatter, body = read_record(path)
        record_type = frontmatter.get("record_type")
        if record_type in {"upstream_feedback", "meta_feedback"}:
            issue = frontmatter.setdefault("issue", {})
            if isinstance(issue, dict):
                issue["provider"] = "github"
                issue["repo"] = repo
                issue["url"] = url
            else:
                frontmatter["issue"] = {"provider": "github", "repo": repo, "url": url}
        elif record_type == "imported_feedback":
            links = frontmatter.setdefault("links", {})
            if isinstance(links, dict):
                links["issue_url"] = url
            else:
                frontmatter["links"] = {"issue_url": url}
        elif record_type == "failure":
            links = frontmatter.setdefault("links", {})
            if isinstance(links, dict):
                links["issue_url"] = url
            else:
                frontmatter["links"] = {"issue_url": url}
        else:
            continue
        path.write_text(dump_record(frontmatter, body), encoding="utf-8", newline="\n")
        updated += 1
    refresh_project_views(project)
    return updated


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
    issue_format = format in {"issue", "github-issue"}
    if issue_format and (not sanitize or allow_private):
        typer.echo(
            "GitHub Issue下書きは --sanitize が必須で、--allow-private とは併用できません"
        )
        raise typer.Exit(1)
    if not sanitize and not allow_private:
        typer.echo("--allow-private なしの未サニタイズエクスポートは拒否します")
        raise typer.Exit(1)
    profile = load_profile(project.profile_id)
    records = []
    target_filter = target or "all"
    for path in sorted((project.overlay_dir / "records/failures").glob("*.md")):
        frontmatter, body = read_record(path)
        disposition = frontmatter.get("disposition", {})
        if disposition.get("type") not in {
            "target-upstream-candidate",
            "meta-harness-candidate",
            "protocol-candidate",
        }:
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
    resolved_targets = sorted(
        {
            str(
                record[1].get("target")
                or record[1].get("disposition", {}).get("target")
                or "unknown"
            )
            for record in records
        }
    )
    export_target = target or (
        "mixed" if len(resolved_targets) != 1 else resolved_targets[0]
    )
    prefix = "MF" if export_target == "harnessops" else "UF"
    out_dir = project.overlay_dir / "views" / "exported-feedback"
    out_dir.mkdir(parents=True, exist_ok=True)
    export_id = next_id(out_dir, prefix)
    title = f"{export_target} へのフィードバック"
    sections = []
    for path, frontmatter, body in records:
        sections.append(
            f"## 送信元 {frontmatter.get('id')}: {path.name}\n\n{body.strip()}\n"
        )
    bundle_body = "\n".join(sections)
    if sanitize:
        bundle_body = sanitize_text(
            bundle_body, root=root, profile=profile, allow_private=allow_private
        )
    if issue_format:
        bundle_body = (
            "## Issue下書き\n\n"
            + bundle_body
            + "\n\n## 確認\n\nこれは下書きのみです。HarnessOps はリモートIssueを自動作成しません。\n"
        )
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
        "source_records": [record[1].get("id") for record in records],
    }
    text = (
        "---\n"
        + json.dumps(frontmatter, indent=2)
        + "\n---\n\n# "
        + title
        + "\n\n"
        + bundle_body
    )
    out_path = out_dir / f"{export_id}-{export_target}-feedback.md"
    out_path.write_text(text, encoding="utf-8", newline="\n")
    refresh_project_views(project)
    typer.echo(project.display_path(out_path))


@issue_app.command("create")
def create_issue(
    bundle: Path = typer.Argument(...),
    repo: str = typer.Option(..., "--repo"),
    confirm_create: bool = typer.Option(False, "--confirm-create"),
    allow_duplicate: bool = typer.Option(False, "--allow-duplicate"),
    title: Optional[str] = typer.Option(None, "--title"),
) -> None:
    """サニタイズ済みGitHub Issue下書きからIssueを作成します。"""
    root = find_root()
    project = load_project(root)
    profile = load_profile(project.profile_id)
    try:
        validate_repo(repo)
    except ValueError as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    bundle_path = _resolve_bundle_path(root, bundle)
    source, body = _load_issue_bundle(root, profile, bundle_path)
    issue_title = _issue_title(source, body, title)

    typer.echo("Issue title:")
    typer.echo(issue_title)
    typer.echo("\nIssue body:")
    typer.echo(body)

    duplicates, search_error = search_duplicate_issues(repo, issue_title)
    if search_error:
        draft_path = _write_fallback_issue_draft(bundle_path, issue_title, body)
        typer.echo(f"\n重複検索をスキップしました: {search_error}")
        typer.echo(
            f"Markdown下書きを書きました: {project.display_path(draft_path)}"
        )
        if confirm_create:
            raise typer.Exit(1)
    elif duplicates:
        typer.echo("\n重複候補:")
        for item in duplicates:
            number = item.get("number", "?")
            found_title = item.get("title", "")
            url = item.get("url", "")
            typer.echo(f"- #{number} {found_title} {url}")
        if confirm_create and not allow_duplicate:
            typer.echo("--allow-duplicate なしでは重複候補があるIssueは作成しません")
            raise typer.Exit(1)
    else:
        typer.echo("\n重複候補は見つかりませんでした")

    if not confirm_create:
        typer.echo(
            "\nリモートIssueは作成していません。作成するには --confirm-create を指定してください。"
        )
        return

    try:
        issue_url = create_github_issue(repo, issue_title, body)
    except RuntimeError as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    updated = _write_issue_url_to_records(
        root,
        bundle_path,
        source,
        repo=repo,
        url=issue_url,
    )
    typer.echo(f"\nGitHub Issueを作成しました: {issue_url}")
    typer.echo(f"Issue URLを書き戻したレコード数: {updated}")


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
        if source.get("record_type") not in {
            "upstream_feedback",
            "meta_feedback",
        } or not source.get("sanitized", False):
            typer.echo(
                "import にはサニタイズ済み upstream_feedback または meta_feedback バンドルが必要です"
            )
            raise typer.Exit(1)
        title = source_path.stem
    else:
        typer.echo("バンドルパスまたは --issue を指定してください")
        raise typer.Exit(1)
    out_path = create_imported_feedback(
        project, source_record=source, body=body, title=title
    )
    refresh_project_views(project)
    typer.echo(project.display_path(out_path))


def register(app: typer.Typer) -> None:
    feedback_app.command("add-failure")(add_failure_command)
    feedback_app.command("add")(add_feedback_command)
    feedback_app.command("route")(route_command)
    feedback_app.add_typer(issue_app, name="issue")
    app.add_typer(feedback_app, name="feedback")
