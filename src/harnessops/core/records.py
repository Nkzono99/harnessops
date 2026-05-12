from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from harnessops.core.project import Project


ID_PREFIXES = {
    "failure": "F",
    "local_workaround": "LW",
    "upstream_feedback": "UF",
    "meta_feedback": "MF",
    "imported_feedback": "FB",
    "eval_case": "E",
    "hypothesis": "H",
    "experiment": "X",
    "decision": "D",
}


RECORD_DIRS = {
    "failure": "records/failures",
    "local_workaround": "records/local-workarounds",
    "upstream_feedback": "records/upstream-feedback",
    "meta_feedback": "records/meta-feedback",
    "imported_feedback": "records/feedback",
    "eval_case": "records/eval-cases",
    "hypothesis": "records/hypotheses",
    "decision": "records/decisions",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return slug or "record"


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text
    data = yaml.safe_load(parts[1]) or {}
    return data, parts[2]


def dump_record(frontmatter: dict[str, Any], body: str) -> str:
    yaml_text = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=False)
    return f"---\n{yaml_text}---\n\n{body.lstrip()}"


def read_record(path: Path) -> tuple[dict[str, Any], str]:
    return split_frontmatter(path.read_text(encoding="utf-8"))


def next_id(directory: Path, prefix: str) -> str:
    directory.mkdir(parents=True, exist_ok=True)
    max_id = 0
    pattern = re.compile(rf"^{re.escape(prefix)}(\d{{4}})")
    for path in directory.glob(f"{prefix}[0-9][0-9][0-9][0-9]*.md"):
        match = pattern.match(path.name)
        if match:
            max_id = max(max_id, int(match.group(1)))
    return f"{prefix}{max_id + 1:04d}"


def record_path(project: Project, record_type: str, record_id: str, title: str) -> Path:
    rel_dir = RECORD_DIRS[record_type]
    return project.overlay_dir / rel_dir / f"{record_id}-{slugify(title)}.md"


def find_record(project: Project, record_or_path: str) -> Path:
    candidate = Path(record_or_path)
    if candidate.exists():
        return candidate
    for path in project.overlay_dir.rglob("*.md"):
        if path.name.startswith(record_or_path):
            return path
        frontmatter, _ = read_record(path)
        if frontmatter.get("id") == record_or_path:
            return path
    raise FileNotFoundError(f"record not found: {record_or_path}")


def create_failure(
    project: Project,
    *,
    title: str,
    target: str | None,
    context: str,
    what_happened: str,
    why_matters: str,
    desired_behavior: str,
    local_workaround: str,
    disposition_type: str,
) -> Path:
    directory = project.overlay_dir / "records/failures"
    record_id = next_id(directory, "F")
    target_value = target or ("harnessops" if disposition_type == "meta-harness-candidate" else None)
    frontmatter = {
        "id": record_id,
        "record_type": "failure",
        "created_at": now_iso(),
        "status": "open",
        "visibility": project.data.get("privacy", {}).get("default_visibility", "private-until-sanitized"),
        "origin": {"repository_kind": project.data.get("project", {}).get("kind"), "profile": project.profile_id},
        "disposition": {"type": disposition_type, "target": target_value, "status": "draft"},
        "privacy": {"contains_private_paths": False, "contains_unpublished_research": False},
        "links": {"upstream_feedback": None, "meta_feedback": None},
    }
    body = f"""# {record_id}: {title}

## Context

{context or "TODO"}

## What happened

{what_happened or "TODO"}

## Why this matters

{why_matters or "TODO"}

## Desired behavior

{desired_behavior or "TODO"}

## Local workaround

{local_workaround or "None recorded."}

## Routing rationale

Initial disposition: `{disposition_type}`.
"""
    path = record_path(project, "failure", record_id, title)
    if path.exists():
        raise FileExistsError(f"record already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_record(frontmatter, body), encoding="utf-8")
    return path


def create_imported_feedback(project: Project, *, source_record: dict[str, Any], body: str, title: str) -> Path:
    directory = project.overlay_dir / "records/feedback"
    record_id = next_id(directory, "FB")
    classification = {
        "failure_class": source_record.get("classification", {}).get("failure_class")
        or source_record.get("failure_class")
        or "unclassified",
        "capability": source_record.get("classification", {}).get("capability") or source_record.get("capability") or "unclassified",
    }
    frontmatter = {
        "id": record_id,
        "record_type": "imported_feedback",
        "created_at": now_iso(),
        "status": "triaged",
        "source": {
            "type": "harness-feedback-export",
            "original_id": source_record.get("id"),
            "source_project": "redacted",
        },
        "classification": classification,
        "links": {"eval_case": None, "issue_url": source_record.get("issue", {}).get("url") if isinstance(source_record.get("issue"), dict) else None},
    }
    record_body = f"""# {record_id}: {title}

## Summary

{body.strip() or "Imported feedback."}

## Reproduction

See source feedback bundle.

## Expected upstream change

See source feedback bundle.
"""
    path = record_path(project, "imported_feedback", record_id, title)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_record(frontmatter, record_body), encoding="utf-8")
    return path


def create_eval_case(project: Project, *, feedback_id: str, title: str, capability: str, failure_class: str) -> Path:
    directory = project.overlay_dir / "records/eval-cases"
    record_id = next_id(directory, "E")
    fixture = directory / "fixtures" / record_id
    fixture.mkdir(parents=True, exist_ok=True)
    (fixture / ".gitkeep").write_text("", encoding="utf-8")
    frontmatter = {
        "id": record_id,
        "record_type": "eval_case",
        "created_at": now_iso(),
        "status": "active",
        "capability": capability,
        "failure_class": failure_class,
        "source_feedback": feedback_id,
    }
    body = f"""# {record_id}: {title}

## Fixture

Fixture directory: `{fixture.relative_to(project.root).as_posix()}`.

## Task

Describe the behavior that should prevent this failure.

## Expected behavior

The target harness handles the failure class without leaking private project context.

## Pass criteria

- The failure condition is detected or prevented.
- The suggested behavior is actionable for upstream maintainers.
- Private project details are not required.

## Fail criteria

- The failure is missed.
- The case requires private context to reproduce.
"""
    path = record_path(project, "eval_case", record_id, title)
    path.write_text(dump_record(frontmatter, body), encoding="utf-8")
    return path


def create_hypothesis(project: Project, *, eval_case_id: str, title: str, capability: str) -> Path:
    directory = project.overlay_dir / "records/hypotheses"
    record_id = next_id(directory, "H")
    frontmatter = {
        "id": record_id,
        "record_type": "hypothesis",
        "created_at": now_iso(),
        "status": "proposed",
        "target_capability": capability,
        "source_eval_case": eval_case_id,
    }
    body = f"""# {record_id}: {title}

## Hypothesis

TODO

## Mechanism

TODO

## Minimal implementation

TODO

## Alternative: deletion or consolidation

TODO

## Expected upside

TODO

## Expected downside

TODO

## Evaluation plan

TODO

## Kill criteria

TODO
"""
    path = record_path(project, "hypothesis", record_id, title)
    path.write_text(dump_record(frontmatter, body), encoding="utf-8")
    return path


def create_decision(project: Project, *, source: str, status: str, title: str) -> Path:
    directory = project.overlay_dir / "records/decisions"
    record_id = next_id(directory, "D")
    frontmatter = {
        "id": record_id,
        "record_type": "decision",
        "created_at": now_iso(),
        "status": status,
        "source": source,
    }
    body = f"""# {record_id}: {title}

## Decision

{status}

## Reason

TODO

## Evidence

TODO

## Regression risk

TODO

## Follow-up

TODO
"""
    path = record_path(project, "decision", record_id, title)
    path.write_text(dump_record(frontmatter, body), encoding="utf-8")
    return path

