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


DEFAULT_MAX_FILES = 256
DEFAULT_MAX_BYTES = 2_000_000
DEFAULT_MAX_IMPROVEMENTS = 50
ABSTRACTION_MANIFEST = "knowledge/lab-memory-abstraction.yml"
ABSTRACTION_INPUT_YML = "knowledge/lab-memory-input.yml"
ABSTRACTION_INPUT_MD = "knowledge/lab-memory-input.md"
ABSTRACTION_TARGETS = [
    {
        "path": "knowledge/principles.md",
        "purpose": "採用/却下を越えて残った設計原則を source ID 付きで保つ。",
    },
    {
        "path": "knowledge/patterns.yml",
        "purpose": "再利用可能な改善パターン、適用条件、反例、ガードを構造化する。",
    },
    {
        "path": "knowledge/anti-patterns.md",
        "purpose": "繰り返し避けるべき改善劇場、過剰一般化、失敗クラスをまとめる。",
    },
    {
        "path": "knowledge/evaluation-playbook.md",
        "purpose": "評価軸、holdout、判断基準、kill criteria の経験をまとめる。",
    },
]

CURATOR_START = "<!-- harnessops:curator-notes:start -->"
CURATOR_END = "<!-- harnessops:curator-notes:end -->"
DEFAULT_CURATOR_NOTES = (
    "ここは `hops lab compact` が保持する手編集領域です。"
    "deterministic snapshot への補足、反例、今後の見直し観点を短く追記できます。"
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
        "research_scan_count": len(list((overlay / "records/research-scans").glob("RS*.md"))),
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


def _rel(project: Project, path: Path) -> str:
    return path.relative_to(project.root).as_posix()


def _one_line(text: object, *, limit: int = 220) -> str:
    value = " ".join(str(text or "").split())
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "..."


def _excerpt(text: str, *, limit: int = 1800) -> str:
    value = text.strip()
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


def _safe_yaml(path: Path) -> dict[str, Any]:
    data = yamlio.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def _snapshot_state(project: Project, current_digest: str) -> dict[str, Any]:
    path = project.overlay_dir / "knowledge" / "lab-memory.yml"
    if not path.exists():
        return {
            "exists": False,
            "path": _rel(project, path),
            "source_digest": None,
            "stale": True,
        }
    data = _safe_yaml(path)
    sources = data.get("sources", {})
    source_digest = sources.get("source_digest") if isinstance(sources, dict) else None
    return {
        "exists": True,
        "path": _rel(project, path),
        "source_digest": source_digest,
        "stale": source_digest != current_digest,
    }


def _abstraction_state(project: Project, current_digest: str) -> dict[str, Any]:
    manifest_path = project.overlay_dir / ABSTRACTION_MANIFEST
    target_states = []
    for target in ABSTRACTION_TARGETS:
        path = project.overlay_dir / target["path"]
        target_states.append(
            {
                "path": _rel(project, path),
                "exists": path.exists(),
                "purpose": target["purpose"],
            }
        )
    if not manifest_path.exists():
        return {
            "exists": False,
            "path": _rel(project, manifest_path),
            "source_digest": None,
            "stale": True,
            "targets": target_states,
            "missing_targets": [item["path"] for item in target_states if not item["exists"]],
        }
    data = _safe_yaml(manifest_path)
    source_digest = data.get("source_digest")
    return {
        "exists": True,
        "path": _rel(project, manifest_path),
        "source_digest": source_digest,
        "stale": source_digest != current_digest,
        "targets": target_states,
        "missing_targets": [item["path"] for item in target_states if not item["exists"]],
    }


def lint_lab_memory(
    project: Project,
    *,
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
    pressure = _threshold_triggers(
        metrics,
        max_files=max_files,
        max_bytes=max_bytes,
        max_improvements=max_improvements,
    )
    current_digest = _source_digest(project)
    snapshot = _snapshot_state(project, current_digest)
    abstraction = _abstraction_state(project, current_digest)
    has_sources = metrics["improvement_count"] > 0 or metrics["research_scan_count"] > 0
    triggers: list[str] = []
    if pressure and has_sources:
        triggers.extend(pressure)
        if not snapshot["exists"]:
            triggers.append("deterministic_snapshot_missing")
        elif snapshot["stale"]:
            triggers.append("deterministic_snapshot_stale")
        if not abstraction["exists"]:
            triggers.append("semantic_memory_missing")
        elif abstraction["stale"]:
            triggers.append("semantic_memory_stale")
        if abstraction["exists"] and abstraction["missing_targets"]:
            triggers.append("semantic_memory_targets_missing")
    status = "needs-abstraction" if triggers else "ok"
    return {
        "schema_version": "0.1",
        "kind": "harness_lab_memory_lint",
        "status": status,
        "reason": "triggers-present" if triggers else "thresholds-not-exceeded-no-sources-or-current",
        "updated_at": now_iso(),
        "metrics": metrics,
        "thresholds": thresholds,
        "source_digest": current_digest,
        "pressure": pressure,
        "triggers": triggers,
        "snapshot": snapshot,
        "abstraction": abstraction,
        "recommended_commands": [
            "hops lab compact --force",
            "hops lab memory prepare --force",
            "Use the hops-compact-lab-memory skill to update abstract knowledge.",
        ],
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
            _one_line(item.get("summary"), limit=240)
            for item in investigations
            if isinstance(item, dict) and item.get("summary")
        ]
        note_lesson = next((card["notes"] for card in reversed(scorecards) if card.get("notes")), "")
        investigation_lesson = investigation_summaries[-1] if investigation_summaries else ""
        observation_lesson = _one_line(section(body, "Source Observation"), limit=240)
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
                "recommendation": _one_line(frontmatter.get("recommendation"), limit=260),
                "candidate_count": len(candidates),
                "candidates": [
                    {
                        "title": _one_line(item.get("title"), limit=160),
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


def _collect_abstraction_sources(project: Project) -> list[dict[str, Any]]:
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
                    "path": _rel(project, path),
                    "status": str(frontmatter.get("status", "unknown")),
                    "maturity": str(frontmatter.get("maturity", "")),
                    "relation": str(frontmatter.get("relation", "")),
                    "promotion_level": str(frontmatter.get("promotion_level", "")),
                    "capability": str(classification.get("capability", "unclassified")),
                    "failure_class": str(classification.get("failure_class", "unclassified")),
                    "digest": sha256_file(path),
                    "excerpt": _excerpt(body),
                }
            )
    return sources


def _abstraction_manifest_template(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "kind": "harness_lab_memory_abstraction",
        "updated_at": "<ISO-8601 timestamp>",
        "source_digest": data["lint"]["source_digest"],
        "sources": [item["id"] for item in data["sources"]],
        "outputs": [target["path"] for target in data["abstraction_targets"]],
        "notes": "Update this manifest when the skill refreshes abstract knowledge.",
    }


def _render_abstraction_input_markdown(data: dict[str, Any]) -> str:
    lint = data["lint"]
    parts = [
        "# Lab Memory Abstraction Input\n",
        "このファイルは `hops lab memory prepare` が作る skill 入力です。",
        "`records/` と `improvements/` が正本で、この bundle は抽象化作業の入口です。\n",
        "## Lint State\n",
        f"- status: {lint['status']}",
        f"- reason: {lint['reason']}",
        f"- source_digest: `{lint['source_digest']}`",
        f"- pressure: {', '.join(lint['pressure']) or 'none'}",
        f"- triggers: {', '.join(lint['triggers']) or 'none'}\n",
        "## Skill Instructions\n",
        "- `hops-compact-lab-memory` skill でこの bundle を読み、抽象知を更新する。",
        "- deterministic snapshot は索引として扱い、採用判断の証拠にはしない。",
        "- すべての原則、パターン、アンチパターン、評価則に source ID を付ける。",
        "- 反例や失敗条件を消さず、適用条件または中止基準として残す。",
        "- 更新後に `lab-memory-abstraction.yml` の `source_digest` をこの値に合わせる。\n",
        "## Abstraction Targets\n",
    ]
    for target in data["abstraction_targets"]:
        parts.append(f"- `{target['path']}`: {target['purpose']}")
    parts.extend(["", "## Sources\n"])
    if not data["sources"]:
        parts.append("抽象化対象の source はありません。")
    for source in data["sources"]:
        parts.append(
            f"### `{source['id']}` {source['capability']}/{source['failure_class']}"
        )
        parts.append(f"- path: `{source['path']}`")
        parts.append(f"- status: {source['status']}")
        if source.get("maturity"):
            parts.append(f"- maturity: {source['maturity']}")
        if source.get("relation"):
            parts.append(f"- relation: {source['relation']}")
        parts.append("")
        parts.append(source["excerpt"])
        parts.append("")
    parts.extend(
        [
            "## Abstraction Manifest Template\n",
            "```yaml",
            yamlio.safe_dump(data["abstraction_manifest_template"], sort_keys=False, allow_unicode=True).strip(),
            "```",
            "",
        ]
    )
    return "\n".join(parts)


def prepare_lab_memory_abstraction(
    project: Project,
    *,
    force: bool = False,
    dry_run: bool = False,
    max_files: int = DEFAULT_MAX_FILES,
    max_bytes: int = DEFAULT_MAX_BYTES,
    max_improvements: int = DEFAULT_MAX_IMPROVEMENTS,
) -> dict[str, Any]:
    lint = lint_lab_memory(
        project,
        max_files=max_files,
        max_bytes=max_bytes,
        max_improvements=max_improvements,
    )
    if not force and lint["status"] == "ok":
        return {
            "status": "skipped",
            "reason": "lint-ok",
            "lint": lint,
            "paths": [],
        }
    knowledge = _build_knowledge(
        project,
        metrics=lint["metrics"],
        thresholds=lint["thresholds"],
        triggers=lint["triggers"],
        mode="abstraction-input",
    )
    data = {
        "schema_version": "0.1",
        "kind": "harness_lab_memory_abstraction_input",
        "updated_at": now_iso(),
        "lint": lint,
        "abstraction_targets": [
            {
                "path": f"{project.overlay_path}/{target['path']}",
                "purpose": target["purpose"],
            }
            for target in ABSTRACTION_TARGETS
        ],
        "deterministic_snapshot": knowledge,
        "sources": _collect_abstraction_sources(project),
    }
    data["abstraction_manifest_template"] = _abstraction_manifest_template(data)
    knowledge_dir = project.overlay_dir / "knowledge"
    yml_path = project.overlay_dir / ABSTRACTION_INPUT_YML
    md_path = project.overlay_dir / ABSTRACTION_INPUT_MD
    if not dry_run:
        knowledge_dir.mkdir(parents=True, exist_ok=True)
        yml_path.write_text(yamlio.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")
        md_path.write_text(_render_abstraction_input_markdown(data), encoding="utf-8", newline="\n")
    return {
        "status": "dry-run" if dry_run else "written",
        "reason": "forced" if force else "lint-triggered",
        "lint": lint,
        "paths": [yml_path, md_path],
    }


def _build_knowledge(
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
            "research_scans": research_scans,
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
        "このファイルは `hops lab compact` が更新する deterministic working index です。",
        "`records/` と `improvements/` は引き続き監査可能な正本で、この snapshot は再利用しやすい索引です。\n",
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
    parts.append("\n## Research Scans\n")
    if knowledge.get("research_scans"):
        for scan in knowledge["research_scans"]:
            parts.append(
                f"- `{scan['id']}` {scan['capability']}/{scan['failure_class']}: "
                f"{scan['recommendation']} ({scan['candidate_count']} candidates)"
            )
    else:
        parts.append("research scan はまだありません。")
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
