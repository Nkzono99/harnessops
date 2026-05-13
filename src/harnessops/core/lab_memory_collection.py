from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
from typing import Any

from harnessops.core import yamlio
from harnessops.core.lock import sha256_file
from harnessops.core.markdown import record_heading, section
from harnessops.core.project import Project
from harnessops.core.record_io import now_iso, read_record


def lab_metrics(project: Project) -> dict[str, int]:
    overlay = project.overlay_dir
    files = [
        path
        for path in overlay.rglob("*")
        if path.is_file() and ".locks" not in path.relative_to(overlay).parts
    ]
    return {
        "file_count": len(files),
        "byte_count": sum(path.stat().st_size for path in files),
        "record_count": len(list((overlay / "records").rglob("*.md"))),
        "feedback_count": len(list((overlay / "records/feedback").glob("FB*.md"))),
        "eval_case_count": len(list((overlay / "records/eval-cases").glob("E*.md"))),
        "hypothesis_count": len(list((overlay / "records/hypotheses").glob("H*.md"))),
        "decision_count": len(list((overlay / "records/decisions").glob("D*.md"))),
        "research_scan_count": len(list((overlay / "records/research-scans").glob("RS*.md"))),
        "improvement_count": len(list((overlay / "improvements").glob("IMP*.md"))),
        "manual_eval_count": len(list((overlay / "views/eval-results").glob("E*-manual-score.yml"))),
    }


def threshold_triggers(
    metrics: dict[str, int],
    *,
    max_files: int,
    max_bytes: int,
    max_improvements: int,
) -> list[str]:
    triggers: list[str] = []
    if metrics["file_count"] > max_files:
        triggers.append(f"file_count>{max_files}")
    if metrics["byte_count"] > max_bytes:
        triggers.append(f"byte_count>{max_bytes}")
    if metrics["improvement_count"] > max_improvements:
        triggers.append(f"improvement_count>{max_improvements}")
    return triggers


def rel_path(project: Project, path: Path) -> str:
    return path.relative_to(project.root).as_posix()


def one_line(text: object, *, limit: int = 220) -> str:
    value = " ".join(str(text or "").split())
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "..."


def excerpt(text: str, *, limit: int = 1800) -> str:
    value = text.strip()
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "..."


def safe_yaml(path: Path) -> dict[str, Any]:
    data = yamlio.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def source_digest(project: Project) -> str:
    source_paths: list[Path] = []
    for rel in ("records", "improvements", "views/eval-results"):
        root = project.overlay_dir / rel
        if root.exists():
            source_paths.extend(path for path in root.rglob("*") if path.is_file())
    digest_items = []
    for path in sorted(source_paths):
        digest_items.append(f"{path.relative_to(project.root).as_posix()}:{sha256_file(path)}")
    return sha256("\n".join(digest_items).encode("utf-8")).hexdigest()


def _manual_eval(project: Project, eval_id: str) -> dict[str, Any] | None:
    yml_path = project.overlay_dir / "views" / "eval-results" / f"{eval_id}-manual-score.yml"
    if not yml_path.exists():
        return None
    data = yamlio.safe_load(yml_path.read_text(encoding="utf-8")) or {}
    scores = data.get("scores", {})
    if not isinstance(scores, dict):
        scores = {}
    return {
        "path": yml_path.relative_to(project.root).as_posix(),
        "scores": scores,
        "notes": one_line(data.get("notes"), limit=260),
    }


def average_scores(scorecards: list[dict[str, Any]]) -> dict[str, float]:
    values: dict[str, list[float]] = defaultdict(list)
    for scorecard in scorecards:
        scores = scorecard.get("scores", {})
        if not isinstance(scores, dict):
            continue
        for key, value in scores.items():
            if isinstance(value, int | float):
                values[str(key)].append(float(value))
    return {
        key: round(sum(items) / len(items), 2)
        for key, items in sorted(values.items())
        if items
    }


def _collect_improvements(project: Project) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in sorted((project.overlay_dir / "improvements").glob("IMP*.md")):
        frontmatter, body = read_record(path)
        classification = frontmatter.get("classification", {})
        if not isinstance(classification, dict):
            classification = {}
        guard = frontmatter.get("guard", {})
        if not isinstance(guard, dict):
            guard = {}
        eval_cases = [str(item) for item in frontmatter.get("eval_cases", []) or []]
        scorecards = [
            scorecard
            for eval_id in eval_cases
            if (scorecard := _manual_eval(project, eval_id)) is not None
        ]
        investigations = frontmatter.get("investigation", [])
        if not isinstance(investigations, list):
            investigations = []
        investigation_summaries = [
            one_line(item.get("summary"), limit=240)
            for item in investigations
            if isinstance(item, dict) and item.get("summary")
        ]
        note_lesson = next((card["notes"] for card in reversed(scorecards) if card.get("notes")), "")
        investigation_lesson = investigation_summaries[-1] if investigation_summaries else ""
        observation_lesson = one_line(section(body, "Source Observation"), limit=240)
        lesson = note_lesson or investigation_lesson or observation_lesson or "No compact lesson recorded yet."
        items.append(
            {
                "id": str(frontmatter.get("id")),
                "title": record_heading(body, path.stem),
                "path": path.relative_to(project.root).as_posix(),
                "status": str(frontmatter.get("status", "unknown")),
                "maturity": str(frontmatter.get("maturity", "raw")),
                "source_type": str(frontmatter.get("source_type", "unknown")),
                "scope": str(frontmatter.get("scope", "unknown")),
                "relation": str(frontmatter.get("relation", "new")),
                "promotion_level": str(frontmatter.get("promotion_level", "unknown")),
                "source_feedback": str(frontmatter.get("source_feedback", "")),
                "eval_cases": eval_cases,
                "hypotheses": [str(item) for item in frontmatter.get("hypotheses", []) or []],
                "decisions": [str(item) for item in frontmatter.get("decisions", []) or []],
                "capability": str(classification.get("capability", "unclassified")),
                "failure_class": str(classification.get("failure_class", "unclassified")),
                "guard": {
                    "status": str(guard.get("status", "not-defined")),
                    "path": guard.get("path"),
                },
                "scorecards": scorecards,
                "average_scores": average_scores(scorecards),
                "investigations": investigation_summaries,
                "external_evidence": [
                    {
                        "source": str(frontmatter.get("id")),
                        "summary": one_line(item.get("summary"), limit=240),
                        "evidence_ref": item.get("evidence_ref"),
                    }
                    for item in investigations
                    if isinstance(item, dict) and item.get("kind") == "external-benchmark"
                ],
                "lesson": lesson,
            }
        )
    return items


def _capability_knowledge(improvements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for item in improvements:
        grouped[item["capability"]][item["failure_class"]].append(item)
    capabilities: list[dict[str, Any]] = []
    for capability, failure_map in sorted(grouped.items()):
        failure_classes: list[dict[str, Any]] = []
        for failure_class, records in sorted(failure_map.items()):
            status_counts = Counter(item["status"] for item in records)
            scorecards = [scorecard for item in records for scorecard in item["scorecards"]]
            guards = [
                {
                    "source": item["id"],
                    "status": item["guard"]["status"],
                    "path": item["guard"].get("path"),
                }
                for item in records
                if item["guard"].get("path") or item["guard"]["status"] != "not-defined"
            ]
            failure_classes.append(
                {
                    "failure_class": failure_class,
                    "improvements": [item["id"] for item in records],
                    "status_counts": dict(sorted(status_counts.items())),
                    "average_scores": average_scores(scorecards),
                    "guards": guards,
                    "lessons": [
                        {"source": item["id"], "status": item["status"], "lesson": item["lesson"]}
                        for item in records
                    ],
                }
            )
        capabilities.append({"capability": capability, "failure_classes": failure_classes})
    return capabilities


def _collect_research_scans(project: Project) -> list[dict[str, Any]]:
    scans: list[dict[str, Any]] = []
    for path in sorted((project.overlay_dir / "records/research-scans").glob("RS*.md")):
        frontmatter, body = read_record(path)
        classification = frontmatter.get("classification", {})
        if not isinstance(classification, dict):
            classification = {}
        candidates = frontmatter.get("candidates", [])
        if not isinstance(candidates, list):
            candidates = []
        scans.append(
            {
                "id": str(frontmatter.get("id")),
                "title": record_heading(body, path.stem),
                "path": path.relative_to(project.root).as_posix(),
                "status": str(frontmatter.get("status", "captured")),
                "scope": str(frontmatter.get("scope", "")),
                "capability": str(classification.get("capability", "unclassified")),
                "failure_class": str(classification.get("failure_class", "unclassified")),
                "recommendation": one_line(frontmatter.get("recommendation"), limit=260),
                "candidate_count": len(candidates),
                "candidates": [
                    {
                        "title": one_line(item.get("title"), limit=160),
                        "relation": item.get("relation"),
                        "recommendation": item.get("recommendation"),
                        "next_command": item.get("next_command"),
                    }
                    for item in candidates
                    if isinstance(item, dict)
                ],
            }
        )
    return scans


def collect_abstraction_sources(project: Project) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for root_rel, pattern in (("improvements", "IMP*.md"), ("records/research-scans", "RS*.md")):
        source_root = project.overlay_dir / root_rel
        for path in sorted(source_root.glob(pattern)):
            frontmatter, body = read_record(path)
            classification = frontmatter.get("classification", {})
            if not isinstance(classification, dict):
                classification = {}
            sources.append(
                {
                    "id": str(frontmatter.get("id", path.stem)),
                    "record_type": str(frontmatter.get("record_type", "unknown")),
                    "title": record_heading(body, path.stem),
                    "path": rel_path(project, path),
                    "status": str(frontmatter.get("status", "unknown")),
                    "maturity": str(frontmatter.get("maturity", "")),
                    "relation": str(frontmatter.get("relation", "")),
                    "promotion_level": str(frontmatter.get("promotion_level", "")),
                    "capability": str(classification.get("capability", "unclassified")),
                    "failure_class": str(classification.get("failure_class", "unclassified")),
                    "digest": sha256_file(path),
                    "excerpt": excerpt(body),
                }
            )
    return sources


def build_knowledge(
    project: Project,
    *,
    metrics: dict[str, int],
    thresholds: dict[str, int],
    triggers: list[str],
    mode: str,
) -> dict[str, Any]:
    improvements = _collect_improvements(project)
    research_scans = _collect_research_scans(project)
    status_counts = Counter(item["status"] for item in improvements)
    guard_index = [
        {
            "source": item["id"],
            "capability": item["capability"],
            "failure_class": item["failure_class"],
            "status": item["guard"]["status"],
            "path": item["guard"].get("path"),
        }
        for item in improvements
        if item["guard"].get("path") or item["guard"]["status"] != "not-defined"
    ]
    external_evidence = [
        evidence
        for item in improvements
        for evidence in item["external_evidence"]
    ]
    contradiction_watch = [
        {
            "source": item["id"],
            "relation": item["relation"],
            "lesson": item["lesson"],
            "path": item["path"],
        }
        for item in improvements
        if item["relation"] in {"contradicts", "regression"}
    ]
    open_questions = [
        {
            "source": item["id"],
            "maturity": item["maturity"],
            "status": item["status"],
            "next": "evaluation-or-decision-needed",
            "path": item["path"],
        }
        for item in improvements
        if item["status"] not in {"adopted", "rejected", "superseded"}
    ]
    return {
        "schema_version": "0.1",
        "kind": "harness_lab_knowledge",
        "updated_at": now_iso(),
        "mutable": True,
        "compaction": {
            "mode": mode,
            "thresholds": thresholds,
            "metrics": metrics,
            "triggers": triggers,
        },
        "sources": {
            "source_digest": source_digest(project),
            "improvements": [item["id"] for item in improvements],
        },
        "knowledge": {
            "summary": {
                "improvement_count": len(improvements),
                "status_counts": dict(sorted(status_counts.items())),
                "capability_count": len({item["capability"] for item in improvements}),
            },
            "capabilities": _capability_knowledge(improvements),
            "research_scans": research_scans,
            "guard_index": guard_index,
            "external_evidence": external_evidence,
            "contradiction_watch": contradiction_watch,
            "open_questions": open_questions,
        },
    }
