from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from harnessops.core.lock import load_lock, sha256_file
from harnessops.core.project import Project
from harnessops.core.record_io import read_record
from harnessops.core.record_types import ID_PREFIXES
from harnessops.core.routing import DISPOSITIONS
from harnessops.profiles.registry import load_profile

EDITABLE_HOPS_FALLBACK = "uv run --with-editable . hops"
BRIDGE_SKILL_PATHS = (
    ".agents/skills/harnessops-bridge/SKILL.md",
    ".claude/skills/harnessops-bridge/SKILL.md",
)

REQUIRED_SECTIONS = {
    "failure": ["文脈", "起きたこと", "重要性", "望ましい挙動", "ローカル回避策", "ルーティング根拠"],
    "upstream_feedback": ["概要", "最小再現", "期待する上流改善", "除外した非公開情報"],
    "meta_feedback": ["概要", "最小再現", "期待する上流改善", "除外した非公開情報"],
    "imported_feedback": ["概要", "再現", "期待する上流変更"],
    "eval_case": ["フィクスチャ", "タスク", "期待される挙動", "合格基準", "不合格基準"],
    "hypothesis": [
        "仮説",
        "メカニズム",
        "最小実装",
        "代替案: 削除または統合",
        "期待される利点",
        "想定される欠点",
        "評価計画",
        "中止基準",
    ],
    "decision": ["判断", "理由", "証拠", "回帰リスク", "フォローアップ", "回帰ガード"],
    "research_scan": ["Scope", "Evidence", "Candidates", "Recommendation", "Next Commands"],
    "improvement_dossier": [
        "Status",
        "Source Observation",
        "Target Capability",
        "Investigation",
        "Evaluation",
        "Hypotheses",
        "Evidence",
        "Guard",
        "Links",
        "Open Questions And Next Action",
        "Decision Log",
    ],
}


def validate_record(path: Path) -> list[str]:
    frontmatter, body = read_record(path)
    errors = []
    for key in ["id", "record_type", "created_at"]:
        if key not in frontmatter:
            errors.append(f"{path}: {key} がありません")
    record_type = frontmatter.get("record_type")
    record_id = str(frontmatter.get("id", ""))
    expected_prefix = ID_PREFIXES.get(str(record_type))
    if expected_prefix and not record_id.startswith(expected_prefix):
        errors.append(f"{path}: idプレフィックスがrecord_typeと一致しません")
    if record_type == "failure":
        for key in ["visibility", "disposition"]:
            if key not in frontmatter:
                errors.append(f"{path}: {key} がありません")
        disposition = frontmatter.get("disposition", {})
        if disposition.get("type") not in DISPOSITIONS:
            errors.append(f"{path}: disposition が不正です")
    if record_type in {"upstream_feedback", "meta_feedback"} and "sanitized" not in frontmatter:
        errors.append(f"{path}: feedback record に sanitized フラグがありません")
    if record_type == "imported_feedback":
        for key in ["source", "classification", "links"]:
            if key not in frontmatter:
                errors.append(f"{path}: imported feedback に {key} がありません")
    if record_type == "eval_case":
        for key in ["capability", "failure_class", "source_feedback"]:
            if key not in frontmatter:
                errors.append(f"{path}: eval case に {key} がありません")
    if record_type == "hypothesis":
        for key in ["target_capability", "source_eval_case"]:
            if key not in frontmatter:
                errors.append(f"{path}: hypothesis に {key} がありません")
    if record_type == "decision":
        if "source" not in frontmatter:
            errors.append(f"{path}: decision に source がありません")
        if frontmatter.get("status") == "adopted":
            evidence = frontmatter.get("evidence", {})
            if not evidence.get("summary") or not evidence.get("guard_path"):
                errors.append(f"{path}: adopted decision には evidence summary と guard_path が必要です")
    if record_type == "research_scan":
        for key in ["scope", "classification", "evidence", "candidates", "recommendation"]:
            if key not in frontmatter:
                errors.append(f"{path}: research scan に {key} がありません")
    if record_type == "improvement_dossier":
        for key in ["source_feedback", "maturity", "scope", "promotion_level", "classification"]:
            if key not in frontmatter:
                errors.append(f"{path}: improvement dossier に {key} がありません")
    for section in REQUIRED_SECTIONS.get(str(record_type), []):
        if f"## {section}" not in body:
            errors.append(f"{path}: セクション {section} がありません")
    if "TODO" in body:
        errors.append(f"{path}: 未解決の TODO プレースホルダーがあります")
    return errors


def _validate_unique_improvement_sources(project: Project) -> list[str]:
    errors: list[str] = []
    seen: dict[str, Path] = {}
    for path in sorted((project.overlay_dir / "improvements").glob("IMP*.md")):
        frontmatter, _ = read_record(path)
        if frontmatter.get("record_type") != "improvement_dossier":
            continue
        source_feedback = frontmatter.get("source_feedback")
        if not source_feedback:
            continue
        source_key = str(source_feedback)
        if source_key in seen:
            first = seen[source_key].relative_to(project.root).as_posix()
            second = path.relative_to(project.root).as_posix()
            errors.append(f"duplicate improvement dossier source_feedback {source_key}: {first}, {second}")
        else:
            seen[source_key] = path
    return errors


def _project_declares_hops_script(root: Path) -> bool:
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return False
    try:
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return False
    project_data = data.get("project", {})
    if not isinstance(project_data, dict):
        return False
    scripts = project_data.get("scripts", {})
    return isinstance(scripts, dict) and "hops" in scripts


def _validate_agent_bridge_invocation(project: Project) -> list[str]:
    if _project_declares_hops_script(project.root):
        return []
    warnings: list[str] = []
    for rel in BRIDGE_SKILL_PATHS:
        path = project.root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if EDITABLE_HOPS_FALLBACK in text:
            warnings.append(
                "agent bridge fallback may be invalid for this repo: "
                f"{rel} uses `{EDITABLE_HOPS_FALLBACK} <command>`, but this repo "
                "does not declare a `hops` console script; run "
                "`uvx --refresh-package harnessops --from harnessops hops update-harness --agent-bridge`."
            )
    return warnings


def doctor(project: Project, *, check_records: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        load_profile(project.profile_id)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"プロファイルが見つかりません: {exc}")
    if not project.overlay_dir.exists():
        errors.append(f"オーバーレイがありません: {project.overlay_path}")
    required_dirs = (
        ["records/failures", "records/local-workarounds", "records/upstream-feedback", "records/meta-feedback", "views"]
        if project.overlay_mode in {"feedback-source", "local-and-feedback"}
        else [
            "records/feedback",
            "records/eval-cases",
            "records/hypotheses",
            "records/decisions",
            "records/research-scans",
            "views",
        ]
    )
    for rel in required_dirs:
        if not (project.overlay_dir / rel).exists():
            errors.append(f"オーバーレイディレクトリがありません: {project.overlay_path}/{rel}")
    lock = load_lock(project.metadata_root)
    if not lock:
        errors.append(".harnessops/lock.json がありません")
    if lock and lock.get("overlay", {}).get("path") != project.overlay_path:
        errors.append("lock の overlay path が project.toml と一致しません")
    managed = lock.get("managed_files", {}) if isinstance(lock.get("managed_files"), dict) else {}
    for rel, expected_hash in managed.items():
        path = project.metadata_root / rel
        if not path.exists():
            errors.append(f"管理対象ファイルがありません: {rel}")
        elif sha256_file(path) != expected_hash:
            warnings.append(f"生成ビューが古いか編集されています: {rel}")
    warnings.extend(_validate_agent_bridge_invocation(project))
    if check_records and project.overlay_dir.exists():
        for path in project.overlay_dir.glob("records/**/*.md"):
            errors.extend(validate_record(path))
        for path in sorted((project.overlay_dir / "improvements").glob("IMP*.md")):
            errors.extend(validate_record(path))
        errors.extend(_validate_unique_improvement_sources(project))
    return {"ok": not errors, "errors": errors, "warnings": warnings}
