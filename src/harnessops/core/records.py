from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import os
from pathlib import Path
import re
import time
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
    "improvement_dossier": "IMP",
}


RECORD_DIRS = {
    "failure": "records/failures",
    "local_workaround": "records/local-workarounds",
    "upstream_feedback": "records/upstream-feedback",
    "meta_feedback": "records/meta-feedback",
    "imported_feedback": "records/feedback",
    "eval_case": "records/eval-cases",
    "hypothesis": "records/hypotheses",
    "experiment": "records/experiments",
    "decision": "records/decisions",
    "improvement_dossier": "improvements",
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
    yaml_text = yamlio.safe_dump(frontmatter, sort_keys=False, allow_unicode=True)
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


def _canonical_record_dirs(record_or_path: str) -> list[Path]:
    dirs: list[Path] = []
    for record_type, prefix in sorted(ID_PREFIXES.items(), key=lambda item: len(item[1]), reverse=True):
        if record_or_path.startswith(prefix):
            dirs.append(Path(RECORD_DIRS[record_type]))
    return dirs


def find_record(project: Project, record_or_path: str) -> Path:
    candidate = Path(record_or_path)
    if candidate.exists():
        return candidate
    for rel_dir in _canonical_record_dirs(record_or_path):
        directory = project.overlay_dir / rel_dir
        for path in sorted(directory.glob(f"{record_or_path}*.md")):
            return path
    for path in project.overlay_dir.rglob("*.md"):
        if path.name.startswith(record_or_path):
            return path
        frontmatter, _ = read_record(path)
        if frontmatter.get("id") == record_or_path:
            return path
    raise FileNotFoundError(f"レコードが見つかりません: {record_or_path}")


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

## 文脈

{context or "作成時点では未入力です。ルーティングまたはエクスポート前に具体的な文脈を追加してください。"}

## 起きたこと

{what_happened or "作成時点では未入力です。ルーティングまたはエクスポート前に観測された挙動を追加してください。"}

## 重要性

{why_matters or "作成時点では未入力です。採用前に能力面またはプライバシー面のリスクを説明してください。"}

## 望ましい挙動

{desired_behavior or "作成時点では未入力です。エクスポート前に期待するハーネス挙動を明記してください。"}

## ローカル回避策

{local_workaround or "記録された回避策はありません。"}

## ルーティング根拠

初期disposition: `{disposition_type}`。
"""
    path = record_path(project, "failure", record_id, title)
    if path.exists():
        raise FileExistsError(f"レコードは既に存在します: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_record(frontmatter, body), encoding="utf-8", newline="\n")
    return path


def create_imported_feedback(project: Project, *, source_record: dict[str, Any], body: str, title: str) -> Path:
    directory = project.overlay_dir / "records/feedback"
    record_id = next_id(directory, "FB")
    classification = {
        "failure_class": source_record.get("classification", {}).get("failure_class")
        or source_record.get("failure_class")
        or "unclassified",
        "capability": source_record.get("classification", {}).get("capability")
        or source_record.get("capability")
        or "unclassified",
    }
    source = {
        "type": "harness-feedback-export",
        "original_id": source_record.get("id"),
        "source_project": "redacted",
    }
    if isinstance(source_record.get("issue"), dict):
        source["issue"] = source_record["issue"]
    frontmatter = {
        "id": record_id,
        "record_type": "imported_feedback",
        "created_at": now_iso(),
        "status": "triaged",
        "source": source,
        "classification": classification,
        "links": {
            "eval_case": None,
            "issue_url": source_record.get("issue", {}).get("url")
            if isinstance(source_record.get("issue"), dict)
            else None,
        },
    }
    record_body = f"""# {record_id}: {title}

## 概要

{body.strip() or "インポート済みフィードバック。"}

## 再現

送信元フィードバックバンドルを参照してください。

## 期待する上流変更

送信元フィードバックバンドルを参照してください。
"""
    path = record_path(project, "imported_feedback", record_id, title)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_record(frontmatter, record_body), encoding="utf-8", newline="\n")
    return path


def create_lab_feedback(
    project: Project,
    *,
    title: str,
    summary: str,
    reproduction: str,
    expected_change: str,
    capability: str,
    failure_class: str,
    source_ref: str | None = None,
) -> Path:
    directory = project.overlay_dir / "records/feedback"
    record_id = next_id(directory, "FB")
    frontmatter = {
        "id": record_id,
        "record_type": "imported_feedback",
        "created_at": now_iso(),
        "status": "triaged",
        "source": {
            "type": "local-capture",
            "original_id": source_ref,
            "source_project": project.data.get("project", {}).get("name", "local"),
        },
        "classification": {
            "capability": capability,
            "failure_class": failure_class,
        },
        "links": {
            "eval_case": None,
            "issue_url": source_ref if source_ref and source_ref.startswith("http") else None,
        },
    }
    record_body = f"""# {record_id}: {title}

## 概要

{summary}

## 再現

{reproduction}

## 期待する上流変更

{expected_change}
"""
    path = record_path(project, "imported_feedback", record_id, title)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_record(frontmatter, record_body), encoding="utf-8", newline="\n")
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
        raise ValueError(f"送信元レコードはfailureではありません: {failure_ref}")
    record_type = feedback_type or ("meta_feedback" if target == "harnessops" else "upstream_feedback")
    if record_type not in {"upstream_feedback", "meta_feedback"}:
        raise ValueError(f"未対応のフィードバック種別です: {record_type}")
    prefix = ID_PREFIXES[record_type]
    directory = project.overlay_dir / RECORD_DIRS[record_type]
    record_id = next_id(directory, prefix)
    feedback_title = title or f"{failure_frontmatter.get('id')} から {target} へのフィードバック"
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
    heading = "HarnessOps へのフィードバック" if record_type == "meta_feedback" else f"{target} へのフィードバック"
    body = f"""# {heading}: {feedback_title}

## 概要

{summary or "失敗レコードから作成したフィードバック下書きです。"}

## 最小再現

`{failure_frontmatter.get('id')}` から導出。

## 期待する上流改善

この失敗クラスを防ぐ最小の上流変更を記述してください。この下書きはサニタイズ付きでエクスポートされるまで共有できません。

## 除外した非公開情報

まだサニタイズされていません。共有前に `hops feedback export --target {target} --sanitize` を実行してください。

## 送信元失敗抜粋

{failure_body.strip()}
"""
    path = record_path(project, record_type, record_id, feedback_title)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_record(frontmatter, body), encoding="utf-8", newline="\n")
    links = failure_frontmatter.setdefault("links", {})
    if record_type == "meta_feedback":
        links["meta_feedback"] = record_id
    else:
        links["upstream_feedback"] = record_id
    failure_path.write_text(dump_record(failure_frontmatter, failure_body), encoding="utf-8", newline="\n")
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

## フィクスチャ

フィクスチャディレクトリ: `{fixture.relative_to(project.root).as_posix()}`。

## タスク

この失敗を防ぐべき挙動を記述してください。

## 期待される挙動

ターゲットハーネスが、非公開プロジェクト文脈を漏らさずに失敗クラスを扱います。

## 合格基準

- 失敗条件が検出または防止される。
- 提案される挙動が上流メンテナにとって実行可能である。
- 非公開プロジェクト詳細を必要としない。

## 不合格基準

- 失敗を見逃す。
- 再現に非公開文脈が必要になる。
"""
    path = record_path(project, "eval_case", record_id, title)
    path.write_text(dump_record(frontmatter, body), encoding="utf-8", newline="\n")
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

## 仮説

{hypothesis or f"評価ケースを失敗させた最小の上流挙動を変更し、`{eval_case_id}` の `{capability}` を改善する。"}

## メカニズム

{mechanism or "採用前に、提案変更が作用するメカニズムを明示してください。曖昧なプロセス追加や文書追加だけでは証拠として不十分です。"}

## 最小実装

{minimal_implementation or "紐づく評価ケースで評価できる最も狭い変更を実装してください。複雑さを減らせるなら、新しい抽象より削除または統合を優先します。"}

## 代替案: 削除または統合

{alternative or "新しい挙動を追加する前に、既存のルール、プロファイル、スキル、テンプレートを削除、統合、厳格化できないか評価してください。"}

## 期待される利点

{expected_upside or f"紐づく評価ケース `{eval_case_id}` が、運用者負担を減らし、プロジェクト固有文脈を上流へ漏らさずに通る。"}

## 想定される欠点

{expected_downside or "想定される欠点: ルーティング摩擦、偽陽性、保守負担が増える可能性。採用にはこの点の明示的な確認が必要です。"}

## 評価計画

{evaluation_plan or f"`hops eval --case {eval_case_id} --manual` を実行し、採用判断を作る前に多軸スコアを記録する。"}

## 中止基準

{kill_criteria or "紐づく評価ケースを改善しない、プライバシーリスクを増やす、または失敗クラスを減らさずにガバナンス構造だけを追加する場合、この仮説を却下または保留する。"}
"""
    path = record_path(project, "hypothesis", record_id, title)
    path.write_text(dump_record(frontmatter, body), encoding="utf-8", newline="\n")
    return path


def _record_heading(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _records_in(project: Project, record_type: str) -> list[tuple[Path, dict[str, Any], str]]:
    paths = sorted((project.overlay_dir / RECORD_DIRS[record_type]).glob("*.md"))
    records = []
    for path in paths:
        frontmatter, body = read_record(path)
        records.append((path, frontmatter, body))
    return records


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
        title = _record_heading(feedback_body, feedback_path.stem)
        path = record_path(project, "improvement_dossier", record_id, title)
        existing_frontmatter = {}

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
            title = _record_heading(record_body, record_path_item.stem)
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
    linked_records = [feedback_id, *eval_ids, *hypothesis_ids, *frontmatter["decisions"]]
    body = f"""# {record_id}: {_record_heading(feedback_body, feedback_path.stem)}

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

{linked_record_section("Evaluation", eval_records, "評価ケースはまだありません。")}

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

## 判断

{status}

## 理由

{reason}

## 証拠

{evidence}

## 回帰リスク

{regression_risk}

## フォローアップ

{follow_up}

## 回帰ガード

{guard_path or "ガードパスは指定されていません。非採用判断では省略できますが、採用済み判断では必須です。"}
"""
    path = record_path(project, "decision", record_id, title)
    path.write_text(dump_record(frontmatter, body), encoding="utf-8", newline="\n")
    return path
