from __future__ import annotations

from pathlib import Path
from typing import Any

from harnessops.core import yamlio
from harnessops.core.overlay import GENERATED_MARKER
from harnessops.core.project import Project
from harnessops.core.records import find_record, now_iso, read_record

DEFAULT_RUBRIC = {
    "impact": 0,
    "mechanism_clarity": 0,
    "evaluability": 0,
    "minimality": 0,
    "regression_risk": 0,
    "operator_burden": 0,
    "anti_theater": 0,
    "maintainability": 0,
    "privacy_sanitization_risk": 0,
}


def parse_scores(items: list[str]) -> dict[str, int]:
    scores = dict(DEFAULT_RUBRIC)
    for item in items:
        if "=" not in item:
            raise ValueError(f"score は dimension=value 形式で指定してください: {item}")
        key, value = item.split("=", 1)
        key = key.strip().replace("-", "_")
        if key not in scores:
            raise ValueError(f"未知のscore軸です: {key}")
        number = int(value)
        if number < 0 or number > 5:
            raise ValueError(f"{key} のscoreは 0..5 で指定してください")
        scores[key] = number
    return scores


def write_manual_eval(project: Project, *, case_id: str, scores: dict[str, int], notes: str, experiment: str | None = None) -> tuple[Path, Path]:
    case_path = find_record(project, case_id)
    frontmatter, body = read_record(case_path)
    if frontmatter.get("record_type") != "eval_case":
        raise ValueError(f"レコードはeval caseではありません: {case_id}")
    result_dir = project.overlay_dir / "views" / "eval-results"
    result_dir.mkdir(parents=True, exist_ok=True)
    eval_id = str(frontmatter.get("id", case_id))
    data: dict[str, Any] = {
        "schema_version": "0.1",
        "record_type": "manual_eval_result",
        "created_at": now_iso(),
        "eval_case": eval_id,
        "experiment": experiment,
        "scores": scores,
        "notes": notes,
        "source_record": case_path.relative_to(project.root).as_posix(),
    }
    yml_path = result_dir / f"{eval_id}-manual-score.yml"
    md_path = result_dir / f"{eval_id}-manual-score.md"
    yml_path.write_text(yamlio.safe_dump(data, sort_keys=False), encoding="utf-8", newline="\n")
    dimensions = "\n".join(f"- {key}: {value}" for key, value in scores.items())
    md_path.write_text(
        GENERATED_MARKER
        + f"# 手動評価結果: {eval_id}\n\n"
        + f"送信元: `{case_path.relative_to(project.root).as_posix()}`\n\n"
        + "## スコア\n\n"
        + dimensions
        + "\n\n## メモ\n\n"
        + (notes or "メモはありません。")
        + "\n\n## 評価ケーススナップショット\n\n"
        + body.strip()
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return yml_path, md_path
