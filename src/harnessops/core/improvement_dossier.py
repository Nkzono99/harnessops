from __future__ import annotations

from contextlib import contextmanager
import os
from pathlib import Path
import time
from typing import Any

from harnessops.core import yamlio
from harnessops.core.markdown import record_heading
from harnessops.core.project import Project
from harnessops.core.record_index import find_record, next_id, record_path
from harnessops.core.record_io import dump_record, now_iso, read_record, slugify
from harnessops.core.record_types import RECORD_DIRS


def _records_in(project: Project, record_type: str) -> list[tuple[Path, dict[str, Any], str]]:
    paths = sorted((project.overlay_dir / RECORD_DIRS[record_type]).glob("*.md"))
    records = []
    for path in paths:
        frontmatter, body = read_record(path)
        records.append((path, frontmatter, body))
    return records


def _manual_eval_summary(project: Project, eval_id: str) -> str:
    result_dir = project.overlay_dir / "views" / "eval-results"
    yml_path = result_dir / f"{eval_id}-manual-score.yml"
    md_path = result_dir / f"{eval_id}-manual-score.md"
    if not yml_path.exists():
        return "- manual_eval: 未実施\n"
    data = yamlio.safe_load(yml_path.read_text(encoding="utf-8")) or {}
    scores = data.get("scores", {})
    score_text = (
        ", ".join(f"{key}={value}" for key, value in scores.items())
        if isinstance(scores, dict)
        else ""
    )
    parts = [f"- manual_eval_yml: `{yml_path.relative_to(project.root).as_posix()}`"]
    if md_path.exists():
        parts.append(f"- manual_eval_md: `{md_path.relative_to(project.root).as_posix()}`")
    if score_text:
        parts.append(f"- scores: {score_text}")
    notes = str(data.get("notes") or "").strip()
    if notes:
        parts.append(f"- notes: {notes}")
    return "\n".join(parts) + "\n"


def _evaluation_section(project: Project, records: list[tuple[Path, dict[str, Any], str]]) -> str:
    if not records:
        return "## Evaluation\n\n評価ケースはまだありません。\n"
    parts = ["## Evaluation\n"]
    for record_path_item, record_frontmatter, record_body in records:
        eval_id = str(record_frontmatter.get("id"))
        rel = record_path_item.relative_to(project.root).as_posix()
        title = record_heading(record_body, record_path_item.stem)
        parts.append(f"### {eval_id}: {title}\n\n")
        parts.append(f"- source: `{rel}`\n")
        parts.append(f"- capability: {record_frontmatter.get('capability', 'unclassified')}\n")
        parts.append(f"- failure_class: {record_frontmatter.get('failure_class', 'unclassified')}\n")
        parts.append(_manual_eval_summary(project, eval_id))
    return "\n".join(parts)


def _feedback_for_record(project: Project, record_ref: str) -> tuple[Path, dict[str, Any], str]:
    path = find_record(project, record_ref)
    frontmatter, body = read_record(path)
    record_type = frontmatter.get("record_type")
    if record_type == "imported_feedback":
        return path, frontmatter, body
    if record_type == "eval_case":
        return _feedback_for_record(project, str(frontmatter.get("source_feedback")))
    if record_type == "hypothesis":
        eval_path = find_record(project, str(frontmatter.get("source_eval_case")))
        eval_frontmatter, _ = read_record(eval_path)
        return _feedback_for_record(project, str(eval_frontmatter.get("source_feedback")))
    if record_type == "decision":
        return _feedback_for_record(project, str(frontmatter.get("source")))
    if record_type == "improvement_dossier":
        return _feedback_for_record(project, str(frontmatter.get("source_feedback")))
    raise ValueError(f"dossier は FB/E/H/D レコードから作成してください: {record_ref}")


def _find_existing_dossier(project: Project, source_feedback: str) -> Path | None:
    for path in sorted((project.overlay_dir / "improvements").glob("IMP*.md")):
        frontmatter, _ = read_record(path)
        if frontmatter.get("source_feedback") == source_feedback:
            return path
    return None


@contextmanager
def _dossier_source_lock(project: Project, source_feedback: str):
    lock_dir = project.overlay_dir / ".locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    lock_path = lock_dir / f"improvement-dossier-{slugify(source_feedback)}.lock"
    stale_after_seconds = 30
    timeout_seconds = 10
    start = time.monotonic()
    fd: int | None = None
    while fd is None:
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode("ascii"))
        except FileExistsError:
            try:
                age = time.time() - lock_path.stat().st_mtime
                if age > stale_after_seconds:
                    lock_path.unlink()
                    continue
            except FileNotFoundError:
                continue
            if time.monotonic() - start > timeout_seconds:
                raise TimeoutError(f"dossier lock timed out: {lock_path}")
            time.sleep(0.05)
    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def _dossier_defaults() -> dict[str, Any]:
    return {
        "source_type": "observation",
        "scope": "harnessops-core",
        "maturity": "raw",
        "relation": "new",
        "promotion_level": "target-lab-case",
        "guard": {"status": "not-defined", "path": None},
        "investigation": [],
    }


def _derived_maturity(decision_status: str, eval_ids: list[str], hypothesis_ids: list[str]) -> str:
    if decision_status in {"adopted", "rejected", "superseded"}:
        return decision_status
    if hypothesis_ids:
        return "hypothesis"
    if eval_ids:
        return "trial"
    return "raw"


def create_or_update_improvement_dossier(project: Project, *, source_ref: str) -> Path:
    feedback_path, feedback_frontmatter, feedback_body = _feedback_for_record(project, source_ref)
    feedback_id = str(feedback_frontmatter.get("id"))
    with _dossier_source_lock(project, feedback_id):
        return _create_or_update_improvement_dossier_from_feedback(
            project,
            feedback_path=feedback_path,
            feedback_frontmatter=feedback_frontmatter,
            feedback_body=feedback_body,
        )


def _create_or_update_improvement_dossier_from_feedback(
    project: Project,
    *,
    feedback_path: Path,
    feedback_frontmatter: dict[str, Any],
    feedback_body: str,
) -> Path:
    feedback_id = str(feedback_frontmatter.get("id"))
    classification = feedback_frontmatter.get("classification", {})
    eval_records = [
        item
        for item in _records_in(project, "eval_case")
        if item[1].get("source_feedback") == feedback_id
    ]
    eval_ids = [str(frontmatter.get("id")) for _, frontmatter, _ in eval_records]
    hypothesis_records = [
        item
        for item in _records_in(project, "hypothesis")
        if item[1].get("source_eval_case") in eval_ids
    ]
    hypothesis_ids = [str(frontmatter.get("id")) for _, frontmatter, _ in hypothesis_records]
    decision_records = [
        item
        for item in _records_in(project, "decision")
        if item[1].get("source") in hypothesis_ids or item[1].get("source") in eval_ids
    ]
    decision_status = (
        str(decision_records[-1][1].get("status"))
        if decision_records
        else "active"
    )
    existing_path = _find_existing_dossier(project, feedback_id)
    if existing_path:
        existing_frontmatter, _ = read_record(existing_path)
        record_id = str(existing_frontmatter.get("id"))
        created_at = existing_frontmatter.get("created_at", now_iso())
        path = existing_path
    else:
        directory = project.overlay_dir / "improvements"
        record_id = next_id(directory, "IMP")
        created_at = now_iso()
        title = record_heading(feedback_body, feedback_path.stem)
        path = record_path(project, "improvement_dossier", record_id, title)
        existing_frontmatter = {}
    research_scan_records = [
        item
        for item in _records_in(project, "research_scan")
        if item[1].get("existing_dossier") in {record_id, feedback_id}
    ]
    research_scan_ids = [str(frontmatter.get("id")) for _, frontmatter, _ in research_scan_records]

    links = feedback_frontmatter.get("links", {})
    source = feedback_frontmatter.get("source", {})
    source_issue = source.get("issue", {}) if isinstance(source, dict) else {}
    issue_url = links.get("issue_url") or source_issue.get("url")
    derived_maturity = _derived_maturity(decision_status, eval_ids, hypothesis_ids)
    existing_maturity = existing_frontmatter.get("maturity")
    maturity = (
        existing_maturity
        if existing_maturity and existing_maturity != "raw"
        else derived_maturity
    )
    defaults = _dossier_defaults()
    frontmatter = {
        "id": record_id,
        "record_type": "improvement_dossier",
        "created_at": created_at,
        "updated_at": now_iso(),
        "status": decision_status,
        "source_type": existing_frontmatter.get("source_type", defaults["source_type"]),
        "scope": existing_frontmatter.get("scope", defaults["scope"]),
        "maturity": maturity,
        "relation": existing_frontmatter.get("relation", defaults["relation"]),
        "promotion_level": existing_frontmatter.get("promotion_level", defaults["promotion_level"]),
        "source_feedback": feedback_id,
        "eval_cases": eval_ids,
        "hypotheses": hypothesis_ids,
        "decisions": [str(item[1].get("id")) for item in decision_records],
        "research_scans": research_scan_ids,
        "classification": {
            "capability": classification.get("capability", "unclassified"),
            "failure_class": classification.get("failure_class", "unclassified"),
        },
        "guard": existing_frontmatter.get("guard", defaults["guard"]),
        "investigation": existing_frontmatter.get("investigation", defaults["investigation"]),
        "links": {"issue_url": issue_url},
    }

    def linked_record_section(
        heading: str,
        records: list[tuple[Path, dict[str, Any], str]],
        empty: str,
    ) -> str:
        if not records:
            return f"## {heading}\n\n{empty}\n"
        parts = [f"## {heading}\n"]
        for record_path_item, record_frontmatter, record_body in records:
            rel = record_path_item.relative_to(project.root).as_posix()
            title = record_heading(record_body, record_path_item.stem)
            parts.append(f"### {record_frontmatter.get('id')}: {title}\n\n")
            parts.append(f"Source: `{rel}`\n\n")
            parts.append(record_body.strip() + "\n")
        return "\n".join(parts)

    feedback_rel = feedback_path.relative_to(project.root).as_posix()
    eval_result_paths = [
        f"harness-lab/views/eval-results/{eval_id}-manual-score.md"
        for eval_id in eval_ids
        if (project.overlay_dir / "views" / "eval-results" / f"{eval_id}-manual-score.md").exists()
    ]
    linked_records = [feedback_id, *research_scan_ids, *eval_ids, *hypothesis_ids, *frontmatter["decisions"]]
    body = f"""# {record_id}: {record_heading(feedback_body, feedback_path.stem)}

## Status

- status: {decision_status}
- maturity: {frontmatter["maturity"]}
- source_type: {frontmatter["source_type"]}
- scope: {frontmatter["scope"]}
- relation: {frontmatter["relation"]}
- promotion_level: {frontmatter["promotion_level"]}
- source_feedback: `{feedback_id}`
- linked_records: {", ".join(f"`{item}`" for item in linked_records) or "none"}

## Source Observation

Source: `{feedback_rel}`

{feedback_body.strip()}

## Target Capability

- capability: {frontmatter["classification"]["capability"]}
- failure_class: {frontmatter["classification"]["failure_class"]}

## Investigation

{_format_investigation(frontmatter["investigation"])}

{linked_record_section("Research Scans", research_scan_records, "research scan はまだありません。")}

{_evaluation_section(project, eval_records)}

{linked_record_section("Hypotheses", hypothesis_records, "仮説はまだありません。")}

## Evidence

{", ".join(f"`{item}`" for item in eval_result_paths) if eval_result_paths else "評価結果はまだありません。"}

## Guard

- status: {frontmatter["guard"].get("status") if isinstance(frontmatter["guard"], dict) else "not-defined"}
- path: {frontmatter["guard"].get("path") if isinstance(frontmatter["guard"], dict) else "未設定"}

## Links

- issue_url: {issue_url or "未設定"}

## Open Questions And Next Action

次の実装または評価ステップは、この dossier と紐づく正規化レコードを更新してから再生成してください。

{linked_record_section("Decision Log", decision_records, "判断レコードはまだありません。")}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_record(frontmatter, body), encoding="utf-8", newline="\n")
    return path


def _format_investigation(items: Any) -> str:
    if not isinstance(items, list) or not items:
        return "調査メモはまだありません。"
    rows = []
    for item in items:
        if not isinstance(item, dict):
            continue
        rows.append(
            "- "
            + f"{item.get('created_at', 'unknown')} "
            + f"[{item.get('kind', 'note')}] "
            + str(item.get("summary", "")).strip()
        )
        evidence_ref = item.get("evidence_ref")
        if evidence_ref:
            rows[-1] += f" (evidence: {evidence_ref})"
    return "\n".join(rows) if rows else "調査メモはまだありません。"


def update_improvement_dossier_metadata(
    project: Project,
    *,
    source_ref: str,
    source_type: str | None = None,
    scope: str | None = None,
    maturity: str | None = None,
    relation: str | None = None,
    promotion_level: str | None = None,
    guard_status: str | None = None,
    guard_path: str | None = None,
) -> Path:
    path = create_or_update_improvement_dossier(project, source_ref=source_ref)
    frontmatter, body = read_record(path)
    for key, value in {
        "source_type": source_type,
        "scope": scope,
        "maturity": maturity,
        "relation": relation,
        "promotion_level": promotion_level,
    }.items():
        if value:
            frontmatter[key] = value
    guard = frontmatter.setdefault("guard", _dossier_defaults()["guard"])
    if not isinstance(guard, dict):
        guard = dict(_dossier_defaults()["guard"])
        frontmatter["guard"] = guard
    if guard_status:
        guard["status"] = guard_status
    if guard_path:
        guard["path"] = guard_path
    path.write_text(dump_record(frontmatter, body), encoding="utf-8", newline="\n")
    return create_or_update_improvement_dossier(project, source_ref=str(frontmatter["source_feedback"]))


def add_improvement_investigation(
    project: Project,
    *,
    source_ref: str,
    summary: str,
    kind: str = "codebase",
    evidence_ref: str | None = None,
) -> Path:
    path = create_or_update_improvement_dossier(project, source_ref=source_ref)
    frontmatter, body = read_record(path)
    items = frontmatter.setdefault("investigation", [])
    if not isinstance(items, list):
        items = []
        frontmatter["investigation"] = items
    items.append(
        {
            "created_at": now_iso(),
            "kind": kind,
            "summary": summary,
            "evidence_ref": evidence_ref,
        }
    )
    if frontmatter.get("maturity") == "raw":
        frontmatter["maturity"] = "investigated"
    path.write_text(dump_record(frontmatter, body), encoding="utf-8", newline="\n")
    return create_or_update_improvement_dossier(project, source_ref=str(frontmatter["source_feedback"]))
