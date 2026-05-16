from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

from harnessops.core import yamlio
from harnessops.core.lab_memory_lint import lint_lab_memory
from harnessops.core.markdown import record_heading
from harnessops.core.project import Project
from harnessops.core.record_io import read_record

ACTIVE_DECISION_STATUSES = {"active", "triaged", "captured", "proposed", "open"}
CLOSED_DECISION_STATUSES = {"adopted", "rejected", "superseded"}
IMPLEMENTED_GUARD_STATUSES = {"implemented", "holdout", "monitoring"}


def _rel(project: Project, path: Path) -> str:
    return path.relative_to(project.root).as_posix()


def _classification(frontmatter: dict[str, Any]) -> dict[str, str]:
    classification = frontmatter.get("classification", {})
    if not isinstance(classification, dict):
        classification = {}
    return {
        "capability": str(classification.get("capability", frontmatter.get("capability", "unclassified"))),
        "failure_class": str(
            classification.get("failure_class", frontmatter.get("failure_class", "unclassified"))
        ),
    }


def _guard(frontmatter: dict[str, Any]) -> dict[str, Any]:
    guard = frontmatter.get("guard", {})
    if not isinstance(guard, dict):
        guard = {}
    return {
        "status": str(guard.get("status", "not-defined")),
        "path": guard.get("path"),
    }


def _manual_eval_exists(project: Project, eval_id: str) -> bool:
    return (project.overlay_dir / "views" / "eval-results" / f"{eval_id}-manual-score.yml").exists()


def _records(project: Project, rel_dir: str, pattern: str) -> list[dict[str, Any]]:
    root = project.overlay_dir / rel_dir
    records: list[dict[str, Any]] = []
    for path in sorted(root.glob(pattern)):
        frontmatter, body = read_record(path)
        records.append(
            {
                "id": str(frontmatter.get("id", path.stem)),
                "record_type": str(frontmatter.get("record_type", "unknown")),
                "title": record_heading(body, path.stem),
                "path": _rel(project, path),
                "frontmatter": frontmatter,
                "body": body,
            }
        )
    return records


def _collect(project: Project) -> dict[str, list[dict[str, Any]]]:
    return {
        "feedback": _records(project, "records/feedback", "FB*.md"),
        "eval_cases": _records(project, "records/eval-cases", "E*.md"),
        "hypotheses": _records(project, "records/hypotheses", "H*.md"),
        "decisions": _records(project, "records/decisions", "D*.md"),
        "improvements": _records(project, "improvements", "IMP*.md"),
        "research_scans": _records(project, "records/research-scans", "RS*.md"),
    }


def _decision_status(records: list[dict[str, Any]], ids: Iterable[str]) -> str | None:
    id_set = {str(item) for item in ids}
    matched = [
        record
        for record in records
        if str(record["frontmatter"].get("source")) in id_set
    ]
    if not matched:
        return None
    return str(matched[-1]["frontmatter"].get("status", "unknown"))


def _queue_item(
    *,
    item_id: str,
    record_type: str,
    title: str,
    path: str,
    priority: int,
    reasons: list[str],
    next_command: str,
    status: str = "",
    maturity: str = "",
    capability: str = "unclassified",
    failure_class: str = "unclassified",
    scope: str = "",
    relation: str = "",
) -> dict[str, Any]:
    return {
        "id": item_id,
        "record_type": record_type,
        "title": title,
        "path": path,
        "priority": priority,
        "reasons": reasons,
        "next_command": next_command,
        "status": status,
        "maturity": maturity,
        "capability": capability,
        "failure_class": failure_class,
        "scope": scope,
        "relation": relation,
    }


def lab_queue(
    project: Project,
    *,
    include_closed: bool = False,
    limit: int | None = None,
    capability: str | None = None,
    scope: str | None = None,
) -> dict[str, Any]:
    data = _collect(project)
    eval_by_feedback: dict[str, list[str]] = {}
    for record in data["eval_cases"]:
        source_feedback = str(record["frontmatter"].get("source_feedback", ""))
        eval_by_feedback.setdefault(source_feedback, []).append(record["id"])
    dossier_sources = {
        str(record["frontmatter"].get("source_feedback", ""))
        for record in data["improvements"]
    }

    items: list[dict[str, Any]] = []
    for record in data["improvements"]:
        frontmatter = record["frontmatter"]
        classification = _classification(frontmatter)
        item_scope = str(frontmatter.get("scope", ""))
        if capability and classification["capability"] != capability:
            continue
        if scope and item_scope != scope:
            continue
        status = str(frontmatter.get("status", "unknown"))
        maturity = str(frontmatter.get("maturity", "raw"))
        relation = str(frontmatter.get("relation", "new"))
        guard = _guard(frontmatter)
        eval_cases = [str(item) for item in frontmatter.get("eval_cases", []) or []]
        hypotheses = [str(item) for item in frontmatter.get("hypotheses", []) or []]
        decisions = [str(item) for item in frontmatter.get("decisions", []) or []]
        reasons: list[str] = []
        priority = 0
        next_command = f"hops lab investigate --from {record['id']} --summary \"<next finding>\""

        if relation in {"contradicts", "regression"}:
            reasons.append("contradiction-review")
            priority += 90
            next_command = f"hops lab investigate --from {record['id']} --kind regression --summary \"<counterexample>\""
        if status == "adopted" and (not guard["path"] or guard["status"] not in IMPLEMENTED_GUARD_STATUSES):
            reasons.append("adopted-without-implemented-guard")
            priority += 85
            next_command = f"hops lab classify --from {record['id']} --guard-status implemented --guard-path <path>"
        if guard["status"] in {"planned", "not-defined"} and guard["path"] and status not in {"rejected", "superseded"}:
            reasons.append("guard-followup")
            priority += 50
            next_command = f"hops lab classify --from {record['id']} --guard-status implemented --guard-path {guard['path']}"
        missing_manual = [eval_id for eval_id in eval_cases if not _manual_eval_exists(project, eval_id)]
        if missing_manual:
            reasons.append("manual-eval-needed")
            priority += 45
            next_command = (
                f"hops lab eval --case {missing_manual[0]} "
                "--manual --score impact=<n> --notes \"<evidence>\""
            )
        if hypotheses and not decisions:
            reasons.append("decision-needed")
            priority += 40
            if not missing_manual:
                next_command = f"hops lab decide --from {hypotheses[-1]} --status parked --reason \"<reason>\""
        if eval_cases and not hypotheses:
            reasons.append("hypothesis-needed")
            priority += 35
            next_command = f"hops lab propose --from {eval_cases[-1]}"
        if not eval_cases and maturity in {"raw", "investigated"} and status not in CLOSED_DECISION_STATUSES:
            reasons.append("eval-design-needed")
            priority += 30
            source_feedback = str(frontmatter.get("source_feedback", ""))
            next_command = f"hops lab eval-case create --from {source_feedback or record['id']}"
        if not reasons and not include_closed and status in CLOSED_DECISION_STATUSES:
            continue
        if not reasons:
            reasons.append("review-ready")
            priority += 10
        items.append(
            _queue_item(
                item_id=record["id"],
                record_type="improvement_dossier",
                title=record["title"],
                path=record["path"],
                priority=priority,
                reasons=reasons,
                next_command=next_command,
                status=status,
                maturity=maturity,
                capability=classification["capability"],
                failure_class=classification["failure_class"],
                scope=item_scope,
                relation=relation,
            )
        )

    for record in data["research_scans"]:
        frontmatter = record["frontmatter"]
        classification = _classification(frontmatter)
        if capability and classification["capability"] != capability:
            continue
        item_scope = str(frontmatter.get("scope", ""))
        if scope and item_scope != scope:
            continue
        candidates = frontmatter.get("candidates", [])
        if not isinstance(candidates, list):
            candidates = []
        next_commands = [
            str(item.get("next_command"))
            for item in candidates
            if isinstance(item, dict) and item.get("next_command")
        ]
        if next_commands:
            items.append(
                _queue_item(
                    item_id=record["id"],
                    record_type="research_scan",
                    title=record["title"],
                    path=record["path"],
                    priority=55,
                    reasons=["research-candidate-routing"],
                    next_command=next_commands[0],
                    status=str(frontmatter.get("status", "captured")),
                    capability=classification["capability"],
                    failure_class=classification["failure_class"],
                    scope=item_scope,
                    relation="scan",
                )
            )

    for record in data["feedback"]:
        if record["id"] in dossier_sources or record["id"] in eval_by_feedback:
            continue
        frontmatter = record["frontmatter"]
        classification = _classification(frontmatter)
        if capability and classification["capability"] != capability:
            continue
        items.append(
            _queue_item(
                item_id=record["id"],
                record_type="imported_feedback",
                title=record["title"],
                path=record["path"],
                priority=25,
                reasons=["unlinked-feedback"],
                next_command=f"hops lab dossier --from {record['id']}",
                status=str(frontmatter.get("status", "triaged")),
                capability=classification["capability"],
                failure_class=classification["failure_class"],
                relation="new",
            )
        )

    items.sort(key=lambda item: (-int(item["priority"]), item["id"]))
    if limit is not None:
        items = items[:limit]
    return {
        "ok": True,
        "kind": "harness_lab_queue",
        "overlay_path": project.overlay_path,
        "count": len(items),
        "items": items,
    }


def _matches_text(value: str, tokens: list[str]) -> bool:
    lower = value.lower()
    return all(token in lower for token in tokens)


def lab_context(
    project: Project,
    *,
    query: str | None = None,
    capability: str | None = None,
    failure_class: str | None = None,
    scope: str | None = None,
    limit: int = 5,
) -> dict[str, Any]:
    data = _collect(project)
    tokens = [token.lower() for token in (query or "").split() if token.strip()]
    related_improvements: list[dict[str, Any]] = []
    for record in data["improvements"]:
        frontmatter = record["frontmatter"]
        classification = _classification(frontmatter)
        if capability and classification["capability"] != capability:
            continue
        if failure_class and classification["failure_class"] != failure_class:
            continue
        if scope and str(frontmatter.get("scope", "")) != scope:
            continue
        searchable = " ".join(
            [
                record["id"],
                record["title"],
                record["body"],
                classification["capability"],
                classification["failure_class"],
                str(frontmatter.get("scope", "")),
                str(frontmatter.get("relation", "")),
                str(frontmatter.get("maturity", "")),
            ]
        )
        if tokens and not _matches_text(searchable, tokens):
            continue
        guard = _guard(frontmatter)
        related_improvements.append(
            {
                "id": record["id"],
                "title": record["title"],
                "path": record["path"],
                "status": str(frontmatter.get("status", "unknown")),
                "maturity": str(frontmatter.get("maturity", "raw")),
                "relation": str(frontmatter.get("relation", "new")),
                "scope": str(frontmatter.get("scope", "")),
                "capability": classification["capability"],
                "failure_class": classification["failure_class"],
                "guard": guard,
                "linked_records": {
                    "source_feedback": frontmatter.get("source_feedback"),
                    "eval_cases": frontmatter.get("eval_cases", []) or [],
                    "hypotheses": frontmatter.get("hypotheses", []) or [],
                    "decisions": frontmatter.get("decisions", []) or [],
                },
            }
        )
    related_improvements = related_improvements[:limit]

    related_ids = {item["id"] for item in related_improvements}
    research_scans: list[dict[str, Any]] = []
    for record in data["research_scans"]:
        frontmatter = record["frontmatter"]
        classification = _classification(frontmatter)
        if capability and classification["capability"] != capability:
            continue
        existing = str(frontmatter.get("existing_dossier") or "")
        if related_ids and existing and existing not in related_ids:
            continue
        searchable = " ".join([record["id"], record["title"], record["body"], classification["capability"]])
        if tokens and not _matches_text(searchable, tokens):
            continue
        candidates = frontmatter.get("candidates", [])
        if not isinstance(candidates, list):
            candidates = []
        research_scans.append(
            {
                "id": record["id"],
                "title": record["title"],
                "path": record["path"],
                "scope": str(frontmatter.get("scope", "")),
                "existing_dossier": frontmatter.get("existing_dossier"),
                "recommendation": frontmatter.get("recommendation"),
                "candidates": candidates[:5],
            }
        )
    research_scans = research_scans[:limit]

    knowledge = _knowledge_context(project, capability=capability, failure_class=failure_class, limit=limit)
    queue = lab_queue(project, include_closed=False, limit=limit, capability=capability, scope=scope)
    recommended_reads = [
        item["path"]
        for item in [*related_improvements, *research_scans, *queue["items"]]
        if item.get("path")
    ]
    seen: set[str] = set()
    deduped_reads = []
    for path in recommended_reads:
        if path in seen:
            continue
        seen.add(path)
        deduped_reads.append(path)
    return {
        "ok": True,
        "kind": "harness_lab_context",
        "query": query,
        "filters": {
            "capability": capability,
            "failure_class": failure_class,
            "scope": scope,
        },
        "related_improvements": related_improvements,
        "research_scans": research_scans,
        "queue": queue["items"],
        "knowledge": knowledge,
        "recommended_reads": deduped_reads[:limit],
    }


def _knowledge_context(
    project: Project,
    *,
    capability: str | None,
    failure_class: str | None,
    limit: int,
) -> dict[str, Any]:
    path = project.overlay_dir / "knowledge" / "lab-memory.yml"
    if not path.exists():
        return {"available": False, "reason": "lab-memory.yml missing"}
    data = yamlio.safe_load(path.read_text(encoding="utf-8")) or {}
    knowledge = data.get("knowledge", {}) if isinstance(data, dict) else {}
    if not isinstance(knowledge, dict):
        return {"available": False, "reason": "invalid lab-memory.yml"}
    capabilities = knowledge.get("capabilities", [])
    if not isinstance(capabilities, list):
        capabilities = []
    matched_capabilities: list[dict[str, Any]] = []
    for item in capabilities:
        if not isinstance(item, dict):
            continue
        if capability and item.get("capability") != capability:
            continue
        failure_classes = item.get("failure_classes", [])
        if not isinstance(failure_classes, list):
            failure_classes = []
        if failure_class:
            failure_classes = [
                failure
                for failure in failure_classes
                if isinstance(failure, dict) and failure.get("failure_class") == failure_class
            ]
        matched_capabilities.append(
            {
                "capability": item.get("capability"),
                "failure_classes": failure_classes[:limit],
            }
        )
    return {
        "available": True,
        "path": _rel(project, path),
        "source_digest": data.get("sources", {}).get("source_digest") if isinstance(data.get("sources"), dict) else None,
        "summary": knowledge.get("summary", {}),
        "capabilities": matched_capabilities[:limit],
        "guard_index": (knowledge.get("guard_index", []) or [])[:limit],
        "contradiction_watch": (knowledge.get("contradiction_watch", []) or [])[:limit],
        "open_questions": (knowledge.get("open_questions", []) or [])[:limit],
    }


def lab_lifecycle_lint(project: Project) -> dict[str, Any]:
    data = _collect(project)
    issues: list[dict[str, Any]] = []
    eval_ids = {record["id"] for record in data["eval_cases"]}
    hypothesis_ids = {record["id"] for record in data["hypotheses"]}
    dossier_sources = {
        str(record["frontmatter"].get("source_feedback", ""))
        for record in data["improvements"]
    }

    for record in data["feedback"]:
        if record["id"] not in dossier_sources:
            issues.append(
                {
                    "severity": "info",
                    "code": "unlinked-feedback",
                    "id": record["id"],
                    "path": record["path"],
                    "message": "feedback has no improvement dossier",
                    "next_command": f"hops lab dossier --from {record['id']}",
                }
            )

    for record in data["eval_cases"]:
        if not _manual_eval_exists(project, record["id"]):
            issues.append(
                {
                    "severity": "warning",
                    "code": "manual-eval-missing",
                    "id": record["id"],
                    "path": record["path"],
                    "message": "eval case has no manual scorecard",
                    "next_command": (
                        f"hops lab eval --case {record['id']} "
                        "--manual --score impact=<n> --notes \"<evidence>\""
                    ),
                }
            )

    decided_sources = {
        str(record["frontmatter"].get("source", ""))
        for record in data["decisions"]
    }
    for record in data["hypotheses"]:
        if record["id"] not in decided_sources:
            issues.append(
                {
                    "severity": "warning",
                    "code": "decision-missing",
                    "id": record["id"],
                    "path": record["path"],
                    "message": "hypothesis has no decision",
                    "next_command": f"hops lab decide --from {record['id']} --status parked --reason \"<reason>\"",
                }
            )

    for record in data["improvements"]:
        frontmatter = record["frontmatter"]
        guard = _guard(frontmatter)
        status = str(frontmatter.get("status", "unknown"))
        eval_cases = [str(item) for item in frontmatter.get("eval_cases", []) or []]
        hypotheses = [str(item) for item in frontmatter.get("hypotheses", []) or []]
        relation = str(frontmatter.get("relation", "new"))
        if status == "adopted" and (not guard["path"] or guard["status"] not in IMPLEMENTED_GUARD_STATUSES):
            issues.append(
                {
                    "severity": "error",
                    "code": "adopted-guard-missing",
                    "id": record["id"],
                    "path": record["path"],
                    "message": "adopted improvement lacks an implemented guard",
                    "next_command": f"hops lab classify --from {record['id']} --guard-status implemented --guard-path <path>",
                }
            )
        if relation in {"contradicts", "regression"}:
            issues.append(
                {
                    "severity": "warning",
                    "code": "contradiction-watch",
                    "id": record["id"],
                    "path": record["path"],
                    "message": "improvement is marked as contradiction/regression and should be reviewed",
                    "next_command": f"hops lab investigate --from {record['id']} --kind regression --summary \"<review>\"",
                }
            )
        for eval_id in eval_cases:
            if eval_id not in eval_ids:
                issues.append(
                    {
                        "severity": "error",
                        "code": "missing-linked-eval",
                        "id": record["id"],
                        "path": record["path"],
                        "message": f"dossier references missing eval case {eval_id}",
                        "next_command": f"hops lab dossier --from {record['id']}",
                    }
                )
        for hypothesis_id in hypotheses:
            if hypothesis_id not in hypothesis_ids:
                issues.append(
                    {
                        "severity": "error",
                        "code": "missing-linked-hypothesis",
                        "id": record["id"],
                        "path": record["path"],
                        "message": f"dossier references missing hypothesis {hypothesis_id}",
                        "next_command": f"hops lab dossier --from {record['id']}",
                    }
                )

    for record in data["research_scans"]:
        frontmatter = record["frontmatter"]
        candidates = frontmatter.get("candidates", [])
        if not isinstance(candidates, list):
            candidates = []
        if any(isinstance(item, dict) and item.get("next_command") for item in candidates):
            issues.append(
                {
                    "severity": "info",
                    "code": "research-candidates-present",
                    "id": record["id"],
                    "path": record["path"],
                    "message": "research scan has candidate next commands",
                    "next_command": "hops lab review queue",
                }
            )

    try:
        memory = lint_lab_memory(project)
    except Exception as exc:  # pragma: no cover - defensive guard for broken labs
        memory = {"status": "unknown", "reason": str(exc)}
    if memory.get("status") != "ok":
        issues.append(
            {
                "severity": "warning",
                "code": "memory-lint",
                "id": "harness-lab",
                "path": f"{project.overlay_path}/knowledge",
                "message": f"lab memory lint reports {memory.get('status')}: {memory.get('reason')}",
                "next_command": "hops lab memory prepare --force",
            }
        )

    severity_order = {"error": 0, "warning": 1, "info": 2}
    issues.sort(key=lambda item: (severity_order.get(str(item["severity"]), 9), str(item["id"]), str(item["code"])))
    status = "ok"
    if any(item["severity"] == "error" for item in issues):
        status = "error"
    elif any(item["severity"] == "warning" for item in issues):
        status = "warning"
    elif issues:
        status = "info"
    return {
        "ok": status in {"ok", "info"},
        "kind": "harness_lab_lifecycle_lint",
        "status": status,
        "issue_count": len(issues),
        "issues": issues,
        "memory": memory,
    }
