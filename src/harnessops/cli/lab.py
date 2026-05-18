from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer

from harnessops.cli.feedback import import_feedback
from harnessops.cli.deprecation import warn_if_deprecated
from harnessops.cli.decide import decide_command
from harnessops.cli.eval import eval_command
from harnessops.cli.propose import propose_command
from harnessops.core.issue_bridge import (
    create_github_issue,
    remaining_private_markers,
    search_duplicate_issues,
    validate_repo,
)
from harnessops.core.lab_compaction import (
    DEFAULT_MAX_BYTES,
    DEFAULT_MAX_FILES,
    DEFAULT_MAX_IMPROVEMENTS,
    compact_lab,
    lint_lab_memory,
    prepare_lab_memory_abstraction,
)
from harnessops.core.lab_archive import pack_lab_archive, plan_lab_archive, verify_lab_archive
from harnessops.core.paths import find_root
from harnessops.core.overlay import refresh_managed_files
from harnessops.core.project import load_project
from harnessops.core.lab_usage import lab_context, lab_lifecycle_lint, lab_queue
from harnessops.core.improvement_dossier import (
    add_improvement_investigation,
    create_or_update_improvement_dossier,
    update_improvement_dossier_metadata,
)
from harnessops.core.lab_records import (
    RETIRED_LAB_RECORD_STATUSES,
    create_eval_case,
    create_lab_feedback,
    create_research_scan,
    retire_lab_record,
)
from harnessops.core.record_index import find_record
from harnessops.core.record_io import dump_record, read_record
from harnessops.core.render import refresh_project_views, refresh_views
from harnessops.core.sanitize import sanitize_text
from harnessops.profiles.registry import load_profile

lab_app = typer.Typer(help="harness-lab レコードを操作します。")
issue_app = typer.Typer(help="harness-lab レコードをGitHub Issueへ橋渡しします。")
memory_app = typer.Typer(help="harness-lab knowledge memory の発火判定と抽象化入力を扱います。")
archive_app = typer.Typer(help="release asset 用の harness-lab archive pack を扱います。")
lifecycle_app = typer.Typer(help="harness-lab の活用・停滞・guard 状態を検査します。")
review_app = typer.Typer(help="harness-lab の queue/context/lint を読むための review 入口です。")
eval_case_app = typer.Typer(help="harness-lab 評価ケースを扱います。")


def _jsonable(value: Any, root: Path) -> Any:
    if isinstance(value, Path):
        try:
            return value.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            return value.as_posix()
    if isinstance(value, dict):
        return {key: _jsonable(item, root) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item, root) for item in value]
    return value


def _echo_json(payload: dict[str, Any], root: Path) -> None:
    typer.echo(json.dumps(_jsonable(payload, root), ensure_ascii=False, indent=2))


def _archive_error(exc: RuntimeError) -> None:
    typer.echo(f"lab archive error: {exc}")
    raise typer.Exit(1) from exc


@lab_app.command("import-feedback", hidden=True)
def import_feedback_alias(path: str) -> None:
    """`hops feedback import` のエイリアスです。"""
    warn_if_deprecated("lab import-feedback", "hops feedback import")
    import_feedback(path=Path(path))


@lab_app.command("import", hidden=True)
def import_alias(path: str) -> None:
    """サニタイズ済みフィードバックバンドルをインポートする短いエイリアスです。"""
    warn_if_deprecated("lab import", "hops feedback import")
    import_feedback(path=Path(path))


@eval_case_app.command("create")
@lab_app.command("new-eval-case", hidden=True)
def new_eval_case(from_id: str = typer.Option(..., "--from"), template: str | None = typer.Option(None, "--template")) -> None:
    """インポート済みフィードバックを評価ケースに変換します。"""
    warn_if_deprecated("lab new-eval-case", "hops lab eval-case create")
    del template
    root = find_root()
    project = load_project(root)
    feedback_path = find_record(project, from_id)
    frontmatter, _ = read_record(feedback_path)
    classification = frontmatter.get("classification", {})
    path = create_eval_case(
        project,
        feedback_id=str(frontmatter.get("id", from_id)),
        title=f"{feedback_path.stem} を評価",
        capability=str(classification.get("capability", "unclassified")),
        failure_class=str(classification.get("failure_class", "unclassified")),
    )
    refresh_project_views(project)
    typer.echo(project.display_path(path))


@lab_app.command("capture")
def capture(
    title: str = typer.Option(..., "--title"),
    summary: str = typer.Option(..., "--summary"),
    expected_change: str = typer.Option(..., "--expected-change"),
    reproduction: str = typer.Option("ローカル改善作業中に観測。", "--reproduction"),
    capability: str = typer.Option("harness_lab_traceability", "--capability"),
    failure_class: str = typer.Option("missing_lab_capture", "--failure-class"),
    source_ref: str | None = typer.Option(None, "--source-ref"),
) -> None:
    """ローカル改善やissue前の観測を harness-lab feedback として記録します。"""
    root = find_root()
    project = load_project(root)
    if project.overlay_mode not in {"upstream-lab", "meta-lab"}:
        typer.echo("lab capture には upstream-lab または meta-lab mode が必要です")
        raise typer.Exit(1)
    path = create_lab_feedback(
        project,
        title=title,
        summary=summary,
        reproduction=reproduction,
        expected_change=expected_change,
        capability=capability,
        failure_class=failure_class,
        source_ref=source_ref,
    )
    refresh_project_views(project)
    typer.echo(project.display_path(path))


@lab_app.command("retire")
def retire(
    from_id: str = typer.Option(..., "--from"),
    reason: str = typer.Option(..., "--reason"),
    status: str = typer.Option("archived", "--status"),
    evidence_ref: str | None = typer.Option(None, "--evidence-ref"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """lab record を削除せず active queue/memory から退役させます。"""
    root = find_root()
    project = load_project(root)
    if status not in RETIRED_LAB_RECORD_STATUSES:
        typer.echo("status は archived または superseded を指定してください")
        raise typer.Exit(1)
    path = retire_lab_record(
        project,
        source_ref=from_id,
        status=status,
        reason=reason,
        evidence_ref=evidence_ref,
    )
    refresh_project_views(project)
    if json_output:
        _echo_json(
            {
                "ok": True,
                "kind": "harness_lab_retirement",
                "id": from_id,
                "status": status,
                "path": path,
                "reason": reason,
                "evidence_ref": evidence_ref,
            },
            root,
        )
        return
    typer.echo(project.display_path(path))


@lab_app.command("dossier")
def dossier(from_id: str = typer.Option(..., "--from")) -> None:
    """FB/E/H/D レコードから1枚の改善 dossier を作成または更新します。"""
    root = find_root()
    project = load_project(root)
    if project.overlay_mode not in {"upstream-lab", "meta-lab"}:
        typer.echo("lab dossier には upstream-lab または meta-lab mode が必要です")
        raise typer.Exit(1)
    path = create_or_update_improvement_dossier(project, source_ref=from_id)
    refresh_project_views(project)
    typer.echo(project.display_path(path))


@lab_app.command("classify")
def classify(
    from_id: str = typer.Option(..., "--from"),
    source_type: str | None = typer.Option(None, "--source-type"),
    scope: str | None = typer.Option(None, "--scope"),
    maturity: str | None = typer.Option(None, "--maturity"),
    relation: str | None = typer.Option(None, "--relation"),
    promotion_level: str | None = typer.Option(None, "--promotion-level"),
    guard_status: str | None = typer.Option(None, "--guard-status"),
    guard_path: str | None = typer.Option(None, "--guard-path"),
) -> None:
    """改善dossierの分類、成熟度、昇格、ガード情報を更新します。"""
    root = find_root()
    project = load_project(root)
    path = update_improvement_dossier_metadata(
        project,
        source_ref=from_id,
        source_type=source_type,
        scope=scope,
        maturity=maturity,
        relation=relation,
        promotion_level=promotion_level,
        guard_status=guard_status,
        guard_path=guard_path,
    )
    refresh_project_views(project)
    typer.echo(project.display_path(path))


@lab_app.command("investigate")
def investigate(
    from_id: str = typer.Option(..., "--from"),
    summary: str = typer.Option(..., "--summary"),
    kind: str = typer.Option("codebase", "--kind"),
    evidence_ref: str | None = typer.Option(None, "--evidence-ref"),
) -> None:
    """改善dossierにコード調査、外部比較、反例などの調査メモを追記します。"""
    root = find_root()
    project = load_project(root)
    path = add_improvement_investigation(
        project,
        source_ref=from_id,
        summary=summary,
        kind=kind,
        evidence_ref=evidence_ref,
    )
    refresh_project_views(project)
    typer.echo(project.display_path(path))


@lab_app.command("research-scan")
def research_scan(
    title: str = typer.Option(..., "--title"),
    scope: str = typer.Option(..., "--scope"),
    capability: str = typer.Option("unclassified", "--capability"),
    failure_class: str = typer.Option("unclassified", "--failure-class"),
    existing_dossier: str | None = typer.Option(None, "--existing-dossier"),
    local_evidence: list[str] = typer.Option(None, "--local-evidence"),
    codebase_evidence: list[str] = typer.Option(None, "--codebase-evidence"),
    external_benchmark: list[str] = typer.Option(None, "--external-benchmark"),
    risk: list[str] = typer.Option(None, "--risk"),
    candidate: list[str] = typer.Option(None, "--candidate"),
    recommendation: str = typer.Option(..., "--recommendation"),
) -> None:
    """メタ改善調査の結果を構造化した research scan として保存します。"""
    root = find_root()
    project = load_project(root)
    if project.overlay_mode not in {"upstream-lab", "meta-lab"}:
        typer.echo("lab research-scan には upstream-lab または meta-lab mode が必要です")
        raise typer.Exit(1)
    path = create_research_scan(
        project,
        title=title,
        scope=scope,
        capability=capability,
        failure_class=failure_class,
        existing_dossier=existing_dossier,
        local_evidence=local_evidence or [],
        codebase_evidence=codebase_evidence or [],
        external_benchmark=external_benchmark or [],
        risk=risk or [],
        candidate=candidate or [],
        recommendation=recommendation,
    )
    refresh_project_views(project)
    typer.echo(project.display_path(path))


@review_app.command("queue")
@lab_app.command("queue", hidden=True)
def queue(
    include_closed: bool = typer.Option(False, "--include-closed"),
    limit: int | None = typer.Option(None, "--limit"),
    capability: str | None = typer.Option(None, "--capability"),
    scope: str | None = typer.Option(None, "--scope"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """harness-lab の記録から priority lane 用の候補 queue を返します。"""
    warn_if_deprecated("lab queue", "hops lab review queue")
    root = find_root()
    project = load_project(root)
    result = lab_queue(
        project,
        include_closed=include_closed,
        limit=limit,
        capability=capability,
        scope=scope,
    )
    if json_output:
        _echo_json(result, root)
        return
    typer.echo(f"items: {result['count']}")
    for item in result["items"]:
        typer.echo(
            f"- {item['id']} p={item['priority']} "
            f"{','.join(item['reasons'])} {item['title']}"
        )
        typer.echo(f"  next: {item['next_command']}")


@review_app.command("context")
@lab_app.command("context", hidden=True)
def context(
    query: str | None = typer.Option(None, "--query"),
    capability: str | None = typer.Option(None, "--capability"),
    failure_class: str | None = typer.Option(None, "--failure-class"),
    scope: str | None = typer.Option(None, "--scope"),
    limit: int = typer.Option(5, "--limit"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """実装前に思い出すべき関連 dossier、判断、guard、knowledge を返します。"""
    warn_if_deprecated("lab context", "hops lab review context")
    root = find_root()
    project = load_project(root)
    result = lab_context(
        project,
        query=query,
        capability=capability,
        failure_class=failure_class,
        scope=scope,
        limit=limit,
    )
    if json_output:
        _echo_json(result, root)
        return
    typer.echo("recommended reads:")
    for path in result["recommended_reads"]:
        typer.echo(f"- {path}")
    if result["queue"]:
        typer.echo("queue:")
        for item in result["queue"]:
            typer.echo(f"- {item['id']} {','.join(item['reasons'])}: {item['next_command']}")


@memory_app.command("compact")
@lab_app.command("compact", hidden=True)
def compact(
    force: bool = typer.Option(False, "--force"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    max_files: int = typer.Option(DEFAULT_MAX_FILES, "--max-files"),
    max_bytes: int = typer.Option(DEFAULT_MAX_BYTES, "--max-bytes"),
    max_improvements: int = typer.Option(DEFAULT_MAX_IMPROVEMENTS, "--max-improvements"),
) -> None:
    """harness-lab を source-linked な deterministic snapshot へ圧縮します。"""
    warn_if_deprecated("lab compact", "hops lab memory compact")
    root = find_root()
    project = load_project(root)
    if project.overlay_mode not in {"upstream-lab", "meta-lab"}:
        typer.echo("lab compact には upstream-lab または meta-lab mode が必要です")
        raise typer.Exit(1)
    result = compact_lab(
        project,
        force=force,
        dry_run=dry_run,
        max_files=max_files,
        max_bytes=max_bytes,
        max_improvements=max_improvements,
    )
    metrics = result["metrics"]
    thresholds = result["thresholds"]
    typer.echo(f"status: {result['status']}")
    typer.echo(f"reason: {result['reason']}")
    typer.echo(
        "metrics: "
        f"files={metrics['file_count']}/{thresholds['max_files']} "
        f"bytes={metrics['byte_count']}/{thresholds['max_bytes']} "
        f"improvements={metrics['improvement_count']}/{thresholds['max_improvements']}"
    )
    if result["triggers"]:
        typer.echo("triggers: " + ", ".join(result["triggers"]))
    if result["paths"]:
        typer.echo("outputs:")
        for path in result["paths"]:
            typer.echo(project.display_path(path))
    elif result["status"] == "skipped":
        typer.echo("--force または小さい閾値を指定すると compaction を手動実行できます")


@memory_app.command("lint")
def memory_lint(
    max_files: int = typer.Option(DEFAULT_MAX_FILES, "--max-files"),
    max_bytes: int = typer.Option(DEFAULT_MAX_BYTES, "--max-bytes"),
    max_improvements: int = typer.Option(DEFAULT_MAX_IMPROVEMENTS, "--max-improvements"),
    json_output: bool = typer.Option(False, "--json"),
    warn_only: bool = typer.Option(False, "--warn-only"),
) -> None:
    """lab memory abstraction を走らせるべきかを判定します。"""
    root = find_root()
    project = load_project(root)
    if project.overlay_mode not in {"upstream-lab", "meta-lab"}:
        typer.echo("lab memory lint には upstream-lab または meta-lab mode が必要です")
        raise typer.Exit(1)
    result = lint_lab_memory(
        project,
        max_files=max_files,
        max_bytes=max_bytes,
        max_improvements=max_improvements,
    )
    if json_output:
        import json

        typer.echo(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        metrics = result["metrics"]
        thresholds = result["thresholds"]
        typer.echo(f"status: {result['status']}")
        typer.echo(f"reason: {result['reason']}")
        typer.echo(
            "metrics: "
            f"files={metrics['file_count']}/{thresholds['max_files']} "
            f"bytes={metrics['byte_count']}/{thresholds['max_bytes']} "
            f"improvements={metrics['improvement_count']}/{thresholds['max_improvements']}"
        )
        typer.echo("pressure: " + (", ".join(result["pressure"]) or "none"))
        typer.echo("triggers: " + (", ".join(result["triggers"]) or "none"))
        typer.echo(f"snapshot: {result['snapshot']['path']} stale={result['snapshot']['stale']}")
        typer.echo(f"abstraction: {result['abstraction']['path']} stale={result['abstraction']['stale']}")
        if result["status"] != "ok":
            typer.echo("next:")
            for command in result["recommended_commands"]:
                typer.echo(f"- {command}")
    if result["status"] != "ok" and not warn_only:
        raise typer.Exit(1)


@memory_app.command("prepare")
def memory_prepare(
    force: bool = typer.Option(False, "--force"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    max_files: int = typer.Option(DEFAULT_MAX_FILES, "--max-files"),
    max_bytes: int = typer.Option(DEFAULT_MAX_BYTES, "--max-bytes"),
    max_improvements: int = typer.Option(DEFAULT_MAX_IMPROVEMENTS, "--max-improvements"),
) -> None:
    """lab memory abstraction skill の入力 bundle を作ります。"""
    root = find_root()
    project = load_project(root)
    if project.overlay_mode not in {"upstream-lab", "meta-lab"}:
        typer.echo("lab memory prepare には upstream-lab または meta-lab mode が必要です")
        raise typer.Exit(1)
    result = prepare_lab_memory_abstraction(
        project,
        force=force,
        dry_run=dry_run,
        max_files=max_files,
        max_bytes=max_bytes,
        max_improvements=max_improvements,
    )
    typer.echo(f"status: {result['status']}")
    typer.echo(f"reason: {result['reason']}")
    typer.echo("lint: " + result["lint"]["status"])
    if result["lint"]["triggers"]:
        typer.echo("triggers: " + ", ".join(result["lint"]["triggers"]))
    if result["paths"]:
        typer.echo("outputs:")
        for path in result["paths"]:
            typer.echo(project.display_path(path))
    elif result["status"] == "skipped":
        typer.echo("--force を指定すると手動で abstraction input を作れます")


@review_app.command("lint")
@lifecycle_app.command("lint")
def lifecycle_lint(
    json_output: bool = typer.Option(False, "--json"),
    warn_only: bool = typer.Option(False, "--warn-only"),
) -> None:
    """harness-lab の未評価、未判断、guard不足、memory圧力を検出します。"""
    warn_if_deprecated("lab lifecycle lint", "hops lab review lint")
    root = find_root()
    project = load_project(root)
    result = lab_lifecycle_lint(project)
    if json_output:
        _echo_json(result, root)
    else:
        typer.echo(f"status: {result['status']}")
        typer.echo(f"issues: {result['issue_count']}")
        for item in result["issues"]:
            typer.echo(
                f"- {item['severity']} {item['code']} {item['id']}: "
                f"{item['message']}"
            )
            typer.echo(f"  next: {item['next_command']}")
    if result["status"] == "error" and not warn_only:
        raise typer.Exit(1)


@archive_app.command("plan")
def archive_plan(
    since_ref: str = typer.Option(..., "--since-ref", "--since-tag"),
    to_ref: str = typer.Option("HEAD", "--to-ref"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """指定ref範囲で削除された harness-lab source records の archive 計画を作ります。"""
    root = find_root()
    project = load_project(root)
    try:
        result = plan_lab_archive(project, since_ref=since_ref, to_ref=to_ref)
    except RuntimeError as exc:
        _archive_error(exc)
    if json_output:
        _echo_json(result, root)
        return
    typer.echo("status: planned")
    typer.echo(f"range: {result['since_ref']}..{result['to_ref']}")
    typer.echo(f"eligible: {result['eligible_count']}")
    typer.echo(f"excluded: {len(result['excluded'])}")
    for entry in result["entries"]:
        typer.echo(f"- {entry['path']} -> {entry['archive_path']}")


@archive_app.command("pack")
def archive_pack(
    since_ref: str = typer.Option(..., "--since-ref", "--since-tag"),
    to_ref: str = typer.Option("HEAD", "--to-ref"),
    out_dir: Path = typer.Option(Path("dist"), "--out"),
    asset_name: str | None = typer.Option(None, "--asset-name"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """削除済み harness-lab source records を release asset 用 zip に詰めます。"""
    root = find_root()
    project = load_project(root)
    try:
        result = pack_lab_archive(
            project,
            since_ref=since_ref,
            to_ref=to_ref,
            out_dir=root / out_dir if not out_dir.is_absolute() else out_dir,
            asset_name=asset_name,
        )
    except RuntimeError as exc:
        _archive_error(exc)
    if json_output:
        _echo_json(result, root)
        return
    typer.echo(f"status: {result['status']}")
    typer.echo(f"eligible: {result['plan']['eligible_count']}")
    if result["path"]:
        path = _jsonable(result["path"], root)
        typer.echo(f"archive: {path}")
        typer.echo(f"sha256: {result['archive_sha256']}")
    else:
        typer.echo("archive: none")


@archive_app.command("verify")
def archive_verify(
    path: Path,
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """harness-lab archive pack の manifest と SHA256SUMS を検証します。"""
    root = find_root()
    archive_path = root / path if not path.is_absolute() else path
    result = verify_lab_archive(archive_path)
    if json_output:
        _echo_json(result, root)
    else:
        typer.echo(f"status: {result['status']}")
        typer.echo(f"entries: {result.get('entry_count', 0)}")
        if result.get("archive_sha256"):
            typer.echo(f"sha256: {result['archive_sha256']}")
        for error in result["errors"]:
            typer.echo(f"- {error}")
    if not result["ok"]:
        raise typer.Exit(1)


def _record_title(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            return title.split(": ", 1)[1] if ": " in title else title
    return fallback


def _lab_issue_source(project, source_ref: str) -> tuple[Path, dict, str, str]:
    source_path = find_record(project, source_ref)
    source_frontmatter, source_body = read_record(source_path)
    if source_frontmatter.get("record_type") != "improvement_dossier":
        try:
            dossier_path = create_or_update_improvement_dossier(project, source_ref=source_ref)
            dossier_frontmatter, dossier_body = read_record(dossier_path)
            return dossier_path, dossier_frontmatter, dossier_body, source_ref
        except ValueError:
            pass
    return source_path, source_frontmatter, source_body, source_ref


def _lab_issue_body(root: Path, project, source_ref: str, title: str | None) -> tuple[Path, dict, str, str]:
    profile = load_profile(project.profile_id)
    source_path, source_frontmatter, source_body, original_ref = _lab_issue_source(project, source_ref)
    issue_title = title or _record_title(source_body, source_path.stem)
    rel = project.display_path(source_path)
    body = f"""## Context

HarnessOps lab record `{original_ref}` was promoted to a GitHub Issue draft.

Source dossier: `{rel}`

## Proposal

{source_body.strip()}

## Safety

This body was sanitized by HarnessOps before issue creation.
"""
    sanitized = sanitize_text(body, root=root, profile=profile)
    markers = remaining_private_markers(root, profile, sanitized)
    if markers:
        typer.echo("GitHub Issue化する前に再サニタイズが必要です: " + ", ".join(markers))
        raise typer.Exit(1)
    return source_path, source_frontmatter, issue_title, sanitized.strip()


def _lab_issue_draft_path(project, source_path: Path) -> Path:
    out_dir = project.overlay_dir / "views" / "lab-issue-drafts"
    out_dir.mkdir(parents=True, exist_ok=True)
    base = out_dir / f"{source_path.stem}-github-issue-draft.md"
    candidate = base
    index = 2
    while candidate.exists():
        candidate = out_dir / f"{source_path.stem}-github-issue-draft-{index}.md"
        index += 1
    return candidate


def _write_issue_url(path: Path, frontmatter: dict, body: str, *, repo: str, url: str) -> None:
    links = frontmatter.setdefault("links", {})
    if not isinstance(links, dict):
        links = {}
        frontmatter["links"] = links
    links["issue_url"] = url
    links["issue_repo"] = repo
    path.write_text(dump_record(frontmatter, body), encoding="utf-8", newline="\n")


def _write_lab_issue_url(root: Path, project, source_path: Path, repo: str, url: str) -> int:
    updated = 0
    source_frontmatter, source_body = read_record(source_path)
    _write_issue_url(source_path, source_frontmatter, source_body, repo=repo, url=url)
    updated += 1
    feedback_id = source_frontmatter.get("source_feedback")
    if source_frontmatter.get("record_type") == "improvement_dossier" and feedback_id:
        try:
            feedback_path = find_record(project, str(feedback_id))
        except FileNotFoundError:
            feedback_path = None
        if feedback_path and feedback_path.resolve() != source_path.resolve():
            feedback_frontmatter, feedback_body = read_record(feedback_path)
            _write_issue_url(feedback_path, feedback_frontmatter, feedback_body, repo=repo, url=url)
            updated += 1
            create_or_update_improvement_dossier(project, source_ref=str(feedback_id))
    refresh_project_views(project)
    return updated


@issue_app.command("draft")
def issue_draft(
    from_id: str = typer.Option(..., "--from"),
    title: str | None = typer.Option(None, "--title"),
) -> None:
    """lab record からサニタイズ済みGitHub Issue下書きを作成します。"""
    root = find_root()
    project = load_project(root)
    source_path, _, issue_title, body = _lab_issue_body(root, project, from_id, title)
    draft_path = _lab_issue_draft_path(project, source_path)
    draft_path.write_text(f"# {issue_title}\n\n{body}\n", encoding="utf-8", newline="\n")
    typer.echo("Issue title:")
    typer.echo(issue_title)
    typer.echo("\nIssue body:")
    typer.echo(body)
    typer.echo(f"\nMarkdown下書きを書きました: {project.display_path(draft_path)}")


@issue_app.command("create")
def issue_create(
    from_id: str = typer.Option(..., "--from"),
    repo: str = typer.Option(..., "--repo"),
    confirm_create: bool = typer.Option(False, "--confirm-create"),
    allow_duplicate: bool = typer.Option(False, "--allow-duplicate"),
    title: str | None = typer.Option(None, "--title"),
) -> None:
    """lab record からGitHub Issueを作成します。"""
    root = find_root()
    project = load_project(root)
    try:
        validate_repo(repo)
    except ValueError as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    source_path, _, issue_title, body = _lab_issue_body(root, project, from_id, title)
    typer.echo("Issue title:")
    typer.echo(issue_title)
    typer.echo("\nIssue body:")
    typer.echo(body)

    duplicates, search_error = search_duplicate_issues(repo, issue_title)
    if search_error:
        draft_path = _lab_issue_draft_path(project, source_path)
        draft_path.write_text(f"# {issue_title}\n\n{body}\n", encoding="utf-8", newline="\n")
        typer.echo(f"\n重複検索をスキップしました: {search_error}")
        typer.echo(f"Markdown下書きを書きました: {project.display_path(draft_path)}")
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
        typer.echo("\nリモートIssueは作成していません。作成するには --confirm-create を指定してください。")
        return

    try:
        issue_url = create_github_issue(repo, issue_title, body)
    except RuntimeError as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    updated = _write_lab_issue_url(root, project, source_path, repo, issue_url)
    typer.echo(f"\nGitHub Issueを作成しました: {issue_url}")
    typer.echo(f"Issue URLを書き戻したレコード数: {updated}")


@lab_app.command("refresh-views")
def refresh_lab_views() -> None:
    """harness-lab の生成ビューを再生成します。"""
    root = find_root()
    project = load_project(root)
    managed = refresh_managed_files(project.storage_root, project.overlay_mode, project.overlay_path)
    written = refresh_views(project.storage_root, project.overlay_path)
    paths = [project.display_path(project.storage_root / rel) for rel in managed["updated"]]
    paths.extend(project.display_path(project.storage_root / item["new"]) for item in managed["written_new"])
    paths.extend(project.display_path(path) for path in written)
    seen: set[str] = set()
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        typer.echo(path)


def register(app: typer.Typer) -> None:
    lab_app.command("propose")(propose_command)
    lab_app.command("eval")(eval_command)
    lab_app.command("decide")(decide_command)
    lab_app.add_typer(eval_case_app, name="eval-case")
    lab_app.add_typer(review_app, name="review")
    lab_app.add_typer(issue_app, name="issue")
    lab_app.add_typer(memory_app, name="memory")
    lab_app.add_typer(archive_app, name="archive")
    lab_app.add_typer(lifecycle_app, name="lifecycle", hidden=True)
    app.add_typer(lab_app, name="lab")
