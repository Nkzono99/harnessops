from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
from typing import Any

from harnessops.core import yamlio
from harnessops.core.lock import sha256_file
from harnessops.core.project import Project
from harnessops.core.records import now_iso, read_record


DEFAULT_MAX_FILES = 256
DEFAULT_MAX_BYTES = 2_000_000
DEFAULT_MAX_IMPROVEMENTS = 50

CURATOR_START = "<!-- harnessops:curator-notes:start -->"
CURATOR_END = "<!-- harnessops:curator-notes:end -->"
DEFAULT_CURATOR_NOTES = (
    "ここは `hops lab compact` が保持する手編集領域です。"
    "圧縮結果への補足、反例、今後の見直し観点を短く追記できます。"
)


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
        "improvement_count": len(list((overlay / "improvements").glob("IMP*.md"))),
        "manual_eval_count": len(list((overlay / "views/eval-results").glob("E*-manual-score.yml"))),
    }


def _threshold_triggers(
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


def _record_heading(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _section(body: str, heading: str) -> str:
    marker = f"## {heading}"
    lines = body.splitlines()
    start: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == marker:
            start = index + 1
            break
    if start is None:
        return ""
    collected: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        collected.append(line)
    return "\n".join(collected).strip()


def _one_line(text: object, *, limit: int = 220) -> str:
    value = " ".join(str(text or "").split())
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "..."


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
        "notes": _one_line(data.get("notes"), limit=260),
    }


def _average_scores(scorecards: list[dict[str, Any]]) -> dict[str, float]:
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


def _source_digest(project: Project) -> str:
    source_paths: list[Path] = []
    for rel in ("records", "improvements", "views/eval-results"):
        root = project.overlay_dir / rel
        if root.exists():
            source_paths.extend(path for path in root.rglob("*") if path.is_file())
    digest_items = []
    for path in sorted(source_paths):
        digest_items.append(f"{path.relative_to(project.root).as_posix()}:{sha256_file(path)}")
    return sha256("\n".join(digest_items).encode("utf-8")).hexdigest()


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
            _one_line(item.get("summary"), limit=240)
            for item in investigations
            if isinstance(item, dict) and item.get("summary")
        ]
        note_lesson = next((card["notes"] for card in reversed(scorecards) if card.get("notes")), "")
        investigation_lesson = investigation_summaries[-1] if investigation_summaries else ""
        observation_lesson = _one_line(_section(body, "Source Observation"), limit=240)
        lesson = note_lesson or investigation_lesson or observation_lesson or "No compact lesson recorded yet."
        items.append(
            {
                "id": str(frontmatter.get("id")),
                "title": _record_heading(body, path.stem),
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
                "average_scores": _average_scores(scorecards),
                "investigations": investigation_summaries,
                "external_evidence": [
                    {
                        "source": str(frontmatter.get("id")),
                        "summary": _one_line(item.get("summary"), limit=240),
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
                    "average_scores": _average_scores(scorecards),
                    "guards": guards,
                    "lessons": [
                        {"source": item["id"], "status": item["status"], "lesson": item["lesson"]}
                        for item in records
                    ],
                }
            )
        capabilities.append({"capability": capability, "failure_classes": failure_classes})
    return capabilities


def _build_knowledge(
    project: Project,
    *,
    metrics: dict[str, int],
    thresholds: dict[str, int],
    triggers: list[str],
    mode: str,
) -> dict[str, Any]:
    improvements = _collect_improvements(project)
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
            "source_digest": _source_digest(project),
            "improvements": [item["id"] for item in improvements],
        },
        "knowledge": {
            "summary": {
                "improvement_count": len(improvements),
                "status_counts": dict(sorted(status_counts.items())),
                "capability_count": len({item["capability"] for item in improvements}),
            },
            "capabilities": _capability_knowledge(improvements),
            "guard_index": guard_index,
            "external_evidence": external_evidence,
            "contradiction_watch": contradiction_watch,
            "open_questions": open_questions,
        },
    }


def _extract_curator_notes(existing: str | None) -> str:
    if not existing or CURATOR_START not in existing or CURATOR_END not in existing:
        return DEFAULT_CURATOR_NOTES
    start = existing.index(CURATOR_START) + len(CURATOR_START)
    end = existing.index(CURATOR_END, start)
    notes = existing[start:end].strip()
    return notes or DEFAULT_CURATOR_NOTES


def _fmt_scores(scores: dict[str, Any]) -> str:
    if not scores:
        return "none"
    return ", ".join(f"{key}={value}" for key, value in scores.items())


def _render_markdown(data: dict[str, Any], curator_notes: str) -> str:
    compaction = data["compaction"]
    knowledge = data["knowledge"]
    metrics = compaction["metrics"]
    thresholds = compaction["thresholds"]
    parts = [
        "# Harness Lab Knowledge\n",
        "このファイルは `hops lab compact` が更新する mutable working memory です。",
        "`records/` と `improvements/` は引き続き監査可能な正本で、この知識層は再利用しやすい要約です。\n",
        "## Compaction State\n",
        f"- updated_at: {data['updated_at']}",
        f"- mode: {compaction['mode']}",
        f"- triggers: {', '.join(compaction['triggers']) or 'forced-or-none'}",
        f"- file_count: {metrics['file_count']} / threshold {thresholds['max_files']}",
        f"- byte_count: {metrics['byte_count']} / threshold {thresholds['max_bytes']}",
        f"- improvement_count: {metrics['improvement_count']} / threshold {thresholds['max_improvements']}",
        f"- source_digest: `{data['sources']['source_digest']}`\n",
        "## How To Use\n",
        "- 作業開始時に全dossierを読む代わりに、まず capability/failure_class の教訓、guard、open question を確認する。",
        "- 採用判断や反例処理では、必ず source ID から正本レコードへ戻る。",
        "- このファイルの Curator Notes は手で更新してよい。次回 compaction でも保持される。\n",
        "## Capability Knowledge\n",
    ]
    capabilities = knowledge["capabilities"]
    if not capabilities:
        parts.append("まだ圧縮できる改善知識はありません。")
    for capability in capabilities:
        parts.append(f"### {capability['capability']}")
        for failure in capability["failure_classes"]:
            parts.append(f"#### {failure['failure_class']}")
            parts.append(f"- sources: {', '.join(f'`{item}`' for item in failure['improvements'])}")
            parts.append(
                "- status_counts: "
                + ", ".join(f"{key}={value}" for key, value in failure["status_counts"].items())
            )
            parts.append(f"- average_scores: {_fmt_scores(failure['average_scores'])}")
            if failure["guards"]:
                guard_text = ", ".join(
                    f"{guard['source']}:{guard['status']}:{guard.get('path') or 'no-path'}"
                    for guard in failure["guards"]
                )
                parts.append(f"- guards: {guard_text}")
            for lesson in failure["lessons"]:
                parts.append(f"- lesson {lesson['source']} ({lesson['status']}): {lesson['lesson']}")
            parts.append("")
    parts.append("## Guard Index\n")
    if knowledge["guard_index"]:
        for guard in knowledge["guard_index"]:
            parts.append(
                f"- `{guard['source']}` {guard['capability']}/{guard['failure_class']}: "
                f"{guard['status']} {guard.get('path') or 'no-path'}"
            )
    else:
        parts.append("ガード付きの改善はまだありません。")
    parts.append("\n## External Evidence\n")
    if knowledge["external_evidence"]:
        for evidence in knowledge["external_evidence"]:
            parts.append(
                f"- `{evidence['source']}` {evidence['summary']} "
                f"(evidence: {evidence.get('evidence_ref') or 'unknown'})"
            )
    else:
        parts.append("外部比較はまだありません。")
    parts.append("\n## Contradictions And Regressions\n")
    if knowledge["contradiction_watch"]:
        for item in knowledge["contradiction_watch"]:
            parts.append(f"- `{item['source']}` relation={item['relation']}: {item['lesson']}")
    else:
        parts.append("既存判断への反例やregressionは記録されていません。")
    parts.append("\n## Open Questions\n")
    if knowledge["open_questions"]:
        for item in knowledge["open_questions"]:
            parts.append(
                f"- `{item['source']}` status={item['status']} maturity={item['maturity']}: {item['next']}"
            )
    else:
        parts.append("未判断の改善テーマはありません。")
    parts.extend(
        [
            "\n## Curator Notes",
            CURATOR_START,
            curator_notes,
            CURATOR_END,
            "",
        ]
    )
    return "\n".join(parts)


def compact_lab(
    project: Project,
    *,
    force: bool = False,
    dry_run: bool = False,
    max_files: int = DEFAULT_MAX_FILES,
    max_bytes: int = DEFAULT_MAX_BYTES,
    max_improvements: int = DEFAULT_MAX_IMPROVEMENTS,
) -> dict[str, Any]:
    metrics = lab_metrics(project)
    thresholds = {
        "max_files": max_files,
        "max_bytes": max_bytes,
        "max_improvements": max_improvements,
    }
    triggers = _threshold_triggers(
        metrics,
        max_files=max_files,
        max_bytes=max_bytes,
        max_improvements=max_improvements,
    )
    if not force and not triggers:
        return {
            "status": "skipped",
            "reason": "thresholds-not-exceeded",
            "metrics": metrics,
            "thresholds": thresholds,
            "triggers": triggers,
            "paths": [],
        }
    mode = "forced" if force else "threshold"
    data = _build_knowledge(project, metrics=metrics, thresholds=thresholds, triggers=triggers, mode=mode)
    knowledge_dir = project.overlay_dir / "knowledge"
    yml_path = knowledge_dir / "lab-memory.yml"
    md_path = knowledge_dir / "lab-memory.md"
    existing_md = md_path.read_text(encoding="utf-8") if md_path.exists() else None
    markdown = _render_markdown(data, _extract_curator_notes(existing_md))
    if not dry_run:
        knowledge_dir.mkdir(parents=True, exist_ok=True)
        yml_path.write_text(yamlio.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")
        md_path.write_text(markdown, encoding="utf-8", newline="\n")
    return {
        "status": "dry-run" if dry_run else "written",
        "reason": "forced" if force else "thresholds-exceeded",
        "metrics": metrics,
        "thresholds": thresholds,
        "triggers": triggers,
        "paths": [yml_path, md_path],
    }
