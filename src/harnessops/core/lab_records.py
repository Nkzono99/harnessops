from __future__ import annotations

from pathlib import Path
from typing import Any

from harnessops.core.markdown import record_heading, section
from harnessops.core.project import Project
from harnessops.core.record_index import find_record, next_id, record_path
from harnessops.core.record_io import dump_record, now_iso, read_record
from harnessops.core.record_types import ID_PREFIXES, RECORD_DIRS


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


def _split_structured_option(value: str, field_count: int) -> list[str]:
    parts = [part.strip() for part in value.split("|")]
    if len(parts) > field_count:
        head = parts[: field_count - 1]
        tail = "|".join(parts[field_count - 1 :]).strip()
        parts = [*head, tail]
    return [*parts, *([""] * (field_count - len(parts)))]


def _parse_evidence_items(values: list[str]) -> list[dict[str, str | None]]:
    items: list[dict[str, str | None]] = []
    for value in values:
        summary, ref = _split_structured_option(value, 2)
        if summary:
            items.append({"summary": summary, "ref": ref or None})
    return items


def _parse_candidate_items(values: list[str]) -> list[dict[str, str | None]]:
    items: list[dict[str, str | None]] = []
    for value in values:
        title, relation, recommendation, next_command = _split_structured_option(value, 4)
        if title:
            items.append(
                {
                    "title": title,
                    "relation": relation or "new",
                    "recommendation": recommendation or "note",
                    "next_command": next_command or None,
                }
            )
    return items


def _format_evidence_group(items: list[dict[str, str | None]]) -> str:
    if not items:
        return "- なし"
    rows = []
    for item in items:
        ref = item.get("ref")
        suffix = f" (ref: {ref})" if ref else ""
        rows.append(f"- {item.get('summary')}{suffix}")
    return "\n".join(rows)


def _format_candidate_table(items: list[dict[str, str | None]]) -> str:
    if not items:
        return "候補は記録されていません。"
    rows = ["| candidate | relation | recommendation | next_command |", "|---|---|---|---|"]
    for item in items:
        rows.append(
            "| "
            + f"{item.get('title')} | "
            + f"{item.get('relation')} | "
            + f"{item.get('recommendation')} | "
            + f"{item.get('next_command') or ''} |"
        )
    return "\n".join(rows)


def create_research_scan(
    project: Project,
    *,
    title: str,
    scope: str,
    capability: str,
    failure_class: str,
    existing_dossier: str | None,
    local_evidence: list[str],
    codebase_evidence: list[str],
    external_benchmark: list[str],
    risk: list[str],
    candidate: list[str],
    recommendation: str,
) -> Path:
    directory = project.overlay_dir / "records/research-scans"
    record_id = next_id(directory, "RS")
    evidence = {
        "local": _parse_evidence_items(local_evidence),
        "codebase": _parse_evidence_items(codebase_evidence),
        "external": _parse_evidence_items(external_benchmark),
        "risk": _parse_evidence_items(risk),
    }
    candidates = _parse_candidate_items(candidate)
    frontmatter = {
        "id": record_id,
        "record_type": "research_scan",
        "created_at": now_iso(),
        "status": "captured",
        "scope": scope,
        "existing_dossier": existing_dossier,
        "classification": {
            "capability": capability,
            "failure_class": failure_class,
        },
        "evidence": evidence,
        "candidates": candidates,
        "recommendation": recommendation,
    }
    next_commands = [
        str(item.get("next_command"))
        for item in candidates
        if item.get("next_command")
    ]
    body = f"""# {record_id}: {title}

## Scope

- scope: {scope}
- existing_dossier: {existing_dossier or "未設定"}
- capability: {capability}
- failure_class: {failure_class}

## Evidence

### Local

{_format_evidence_group(evidence["local"])}

### Codebase

{_format_evidence_group(evidence["codebase"])}

### External

{_format_evidence_group(evidence["external"])}

### Risk And Counterexample

{_format_evidence_group(evidence["risk"])}

## Candidates

{_format_candidate_table(candidates)}

## Recommendation

{recommendation}

## Next Commands

{chr(10).join(f"- `{command}`" for command in next_commands) if next_commands else "次のCLIコマンドは未設定です。"}
"""
    path = record_path(project, "research_scan", record_id, title)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_record(frontmatter, body), encoding="utf-8", newline="\n")
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
    feedback_path = find_record(project, feedback_id)
    _, feedback_body = read_record(feedback_path)
    summary = section(feedback_body, "概要") or record_heading(feedback_body, feedback_path.stem)
    reproduction = section(feedback_body, "再現") or "再現条件は source feedback を参照してください。"
    expected_change = (
        section(feedback_body, "期待する上流変更")
        or section(feedback_body, "期待する上流改善")
        or "期待される変更は source feedback を参照してください。"
    )
    feedback_rel = feedback_path.relative_to(project.root).as_posix()
    fixture_rel = fixture.relative_to(project.root).as_posix()
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

- source_feedback: `{feedback_rel}`
- fixture_dir: `{fixture_rel}`
- observation: {summary}

## タスク

`{capability}` の `{failure_class}` を減らす最小変更を設計または実装し、次の再現条件が解消されるか評価してください。

{reproduction}

## 期待される挙動

{expected_change}

## 合格基準

- `{failure_class}` の再現条件が検出または防止される。
- 提案または実装される変更が source feedback の期待変更に対応している。
- `hops lab eval --case {record_id} --manual` の score と notes で採用判断に必要な証拠を説明できる。
- 非公開プロジェクト詳細を追加で要求しない。

## 不合格基準

- `{failure_class}` の再現条件を見逃す。
- source feedback の期待変更と無関係な改善案になる。
- 評価が yml score へ記録されず、採用判断の証拠として追えない。
- 再現または判断に非公開文脈が必要になる。
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

{evaluation_plan or f"`hops lab eval --case {eval_case_id} --manual` を実行し、採用判断を作る前に多軸スコアを記録する。"}

## 中止基準

{kill_criteria or "紐づく評価ケースを改善しない、プライバシーリスクを増やす、または失敗クラスを減らさずにガバナンス構造だけを追加する場合、この仮説を却下または保留する。"}
"""
    path = record_path(project, "hypothesis", record_id, title)
    path.write_text(dump_record(frontmatter, body), encoding="utf-8", newline="\n")
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
