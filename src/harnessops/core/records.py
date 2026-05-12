from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from harnessops.core import yamlio

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
    data = yamlio.safe_load(parts[1]) or {}
    return data, parts[2]


def dump_record(frontmatter: dict[str, Any], body: str) -> str:
    yaml_text = yamlio.safe_dump(frontmatter, sort_keys=False, allow_unicode=False)
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

{context or "Not supplied at creation time. Add concrete context before routing or export."}

## What happened

{what_happened or "Not supplied at creation time. Add the observed behavior before routing or export."}

## Why this matters

{why_matters or "Not supplied at creation time. Explain the capability or privacy risk before adoption."}

## Desired behavior

{desired_behavior or "Not supplied at creation time. State the expected harness behavior before export."}

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


def create_feedback_from_failure(
    project: Project,
    *,
    failure_ref: str,
    target: str,
    feedback_type: str | None = None,
    title: str | None = None,
    summary: str = "",
) -> Path:
    failure_path = find_record(project, failure_ref)
    failure_frontmatter, failure_body = read_record(failure_path)
    if failure_frontmatter.get("record_type") != "failure":
        raise ValueError(f"source record is not a failure: {failure_ref}")
    record_type = feedback_type or ("meta_feedback" if target == "harnessops" else "upstream_feedback")
    if record_type not in {"upstream_feedback", "meta_feedback"}:
        raise ValueError(f"unsupported feedback type: {record_type}")
    prefix = ID_PREFIXES[record_type]
    directory = project.overlay_dir / RECORD_DIRS[record_type]
    record_id = next_id(directory, prefix)
    feedback_title = title or f"Feedback to {target} from {failure_frontmatter.get('id')}"
    frontmatter = {
        "id": record_id,
        "record_type": record_type,
        "created_at": now_iso(),
        "status": "draft",
        "target": target,
        "source_failure": failure_frontmatter.get("id"),
        "sanitized": False,
        "visibility": failure_frontmatter.get("visibility", "private-until-sanitized"),
        "issue": {"provider": "github", "url": None},
    }
    heading = "Feedback to HarnessOps" if record_type == "meta_feedback" else f"Feedback to {target}"
    body = f"""# {heading}: {feedback_title}

## Summary

{summary or "Draft feedback created from failure record."}

## Minimal reproduction

Derived from `{failure_frontmatter.get('id')}`.

## Expected upstream improvement

State the smallest upstream change that would prevent this failure class. This draft is not shareable until exported with sanitization.

## Private info excluded

Not sanitized yet. Run `hops feedback export --target {target} --sanitize` before sharing.

## Source failure excerpt

{failure_body.strip()}
"""
    path = record_path(project, record_type, record_id, feedback_title)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_record(frontmatter, body), encoding="utf-8")
    links = failure_frontmatter.setdefault("links", {})
    if record_type == "meta_feedback":
        links["meta_feedback"] = record_id
    else:
        links["upstream_feedback"] = record_id
    failure_path.write_text(dump_record(failure_frontmatter, failure_body), encoding="utf-8")
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


def create_hypothesis(
    project: Project,
    *,
    eval_case_id: str,
    title: str,
    capability: str,
    hypothesis: str = "",
    mechanism: str = "",
    minimal_implementation: str = "",
    alternative: str = "",
    expected_upside: str = "",
    expected_downside: str = "",
    evaluation_plan: str = "",
    kill_criteria: str = "",
) -> Path:
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

{hypothesis or f"Improve `{capability}` for `{eval_case_id}` by changing the smallest upstream behavior that caused the eval case to fail."}

## Mechanism

{mechanism or "The proposed change must name the mechanism before adoption. A vague process or documentation addition is insufficient evidence."}

## Minimal implementation

{minimal_implementation or "Implement the narrowest change that can be evaluated by the linked eval case; prefer deletion or consolidation over a new abstraction when it removes complexity."}

## Alternative: deletion or consolidation

{alternative or "Before adding new behavior, evaluate whether an existing rule, profile, skill, or template can be deleted, merged, or tightened instead."}

## Expected upside

{expected_upside or f"The linked eval case `{eval_case_id}` should pass with less operator burden and without leaking project-specific context upstream."}

## Expected downside

{expected_downside or "Possible downside: more routing friction, false positives, or maintenance burden. Adoption requires checking this explicitly."}

## Evaluation plan

{evaluation_plan or f"Run `hops eval --case {eval_case_id} --manual` and record multi-axis scores before creating an adoption decision."}

## Kill criteria

{kill_criteria or "Reject or park this hypothesis if it does not improve the linked eval case, increases privacy risk, or adds governance structure without reducing a failure class."}
"""
    path = record_path(project, "hypothesis", record_id, title)
    path.write_text(dump_record(frontmatter, body), encoding="utf-8")
    return path


def create_decision(
    project: Project,
    *,
    source: str,
    status: str,
    title: str,
    reason: str,
    evidence: str,
    regression_risk: str,
    follow_up: str,
    guard_path: str | None = None,
) -> Path:
    directory = project.overlay_dir / "records/decisions"
    record_id = next_id(directory, "D")
    frontmatter = {
        "id": record_id,
        "record_type": "decision",
        "created_at": now_iso(),
        "status": status,
        "source": source,
        "evidence": {"summary": evidence, "guard_path": guard_path},
    }
    body = f"""# {record_id}: {title}

## Decision

{status}

## Reason

{reason}

## Evidence

{evidence}

## Regression risk

{regression_risk}

## Follow-up

{follow_up}

## Regression guard

{guard_path or "No guard path was supplied. Non-adopted decisions may omit a guard; adopted decisions must provide one."}
"""
    path = record_path(project, "decision", record_id, title)
    path.write_text(dump_record(frontmatter, body), encoding="utf-8")
    return path
