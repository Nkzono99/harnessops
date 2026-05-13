from __future__ import annotations

from typing import Any

from harnessops.core import yamlio


CURATOR_START = "<!-- harnessops:curator-notes:start -->"
CURATOR_END = "<!-- harnessops:curator-notes:end -->"
DEFAULT_CURATOR_NOTES = (
    "ここは `hops lab compact` が保持する手編集領域です。"
    "deterministic snapshot への補足、反例、今後の見直し観点を短く追記できます。"
)


def abstraction_manifest_template(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "kind": "harness_lab_memory_abstraction",
        "updated_at": "<ISO-8601 timestamp>",
        "source_digest": data["lint"]["source_digest"],
        "sources": [item["id"] for item in data["sources"]],
        "outputs": [target["path"] for target in data["abstraction_targets"]],
        "notes": "Update this manifest when the skill refreshes abstract knowledge.",
    }


def render_abstraction_input_markdown(data: dict[str, Any]) -> str:
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


def extract_curator_notes(existing: str | None) -> str:
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


def render_markdown(data: dict[str, Any], curator_notes: str) -> str:
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
