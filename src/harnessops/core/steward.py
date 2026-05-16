from __future__ import annotations

from datetime import datetime
import json
import subprocess
from pathlib import Path
from typing import Any

from harnessops.core.lab_memory_lint import lint_lab_memory
from harnessops.core.migration import check_migrations
from harnessops.core.project import Project
from harnessops.core.validation import doctor as doctor_project

LANE_RESULT_CONTRACT = [
    "status",
    "changed_files",
    "records_created_or_updated",
    "issues_touched",
    "validation",
    "recommended_next",
    "stop_reason",
]
LANE_RESULT_STATUSES = {"completed", "no-op", "blocked", "failed-validation"}
RUN_END_STATUSES = {"completed", "blocked", "failed-validation", "no-op"}

SUPERVISOR_LANES = [
    {
        "lane": "maintenance",
        "skill": "hops-maintenance-steward",
        "summary": "HOPS/update-harness, doctor/migrate repair, and safe lab/view/memory maintenance.",
    },
    {
        "lane": "issue-execution",
        "skill": "hops-issue-execution-steward",
        "summary": "Open issue triage, durable HOPS records, and safe issue execution.",
    },
    {
        "lane": "invention",
        "skill": "hops-invention-steward",
        "summary": "Open meta scan, evidence/routing, research records, and lab queue organization.",
    },
    {
        "lane": "priority-improvement",
        "skill": "hops-priority-improvement-steward",
        "summary": "Important recorded improvements, eval/hypothesis/decision/guard, and implementation packets.",
    },
    {
        "lane": "finalize",
        "skill": "hops-finalize-steward",
        "summary": "Validation, automation branch, PR, merge, authorized issue actions, and release criteria.",
    },
]


def _run_git(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _git_stdout(root: Path, args: list[str]) -> str | None:
    result = _run_git(root, args)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _git_required(root: Path, args: list[str]) -> str:
    result = _run_git(root, args)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise RuntimeError(detail)
    return result.stdout.strip()


def _git_status_lines(root: Path) -> list[str]:
    status = _git_stdout(root, ["status", "--porcelain"]) or ""
    return [line for line in status.splitlines() if line]


def _now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _steward_runs_dir(project: Project) -> Path:
    return project.root / ".harnessops" / "cache" / "steward-runs"


def _ledger_path(project: Project, run_id: str) -> Path:
    if not run_id or any(separator in run_id for separator in ("/", "\\", ":")):
        raise ValueError("invalid run_id")
    return _steward_runs_dir(project) / f"{run_id}.json"


def _relative_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _new_run_id(project: Project) -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    head = (_git_stdout(project.root, ["rev-parse", "--short", "HEAD"]) or "nogit").strip()
    base = f"{timestamp}-{head}"
    candidate = base
    counter = 2
    while _ledger_path(project, candidate).exists():
        candidate = f"{base}-{counter}"
        counter += 1
    return candidate


def _read_ledger(project: Project, run_id: str) -> tuple[Path, dict[str, Any]]:
    path = _ledger_path(project, run_id)
    if not path.exists():
        raise FileNotFoundError(f"steward run ledger not found: {run_id}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("steward run ledger is not an object")
    return path, data


def _ahead_behind(root: Path) -> tuple[int, int] | None:
    counts = _git_stdout(root, ["rev-list", "--left-right", "--count", "HEAD...@{u}"])
    if not counts:
        return None
    parts = counts.split()
    if len(parts) != 2:
        return None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None


def _line_count(root: Path, rel: str, pattern: str) -> int:
    directory = root / rel
    if not directory.exists():
        return 0
    return len(list(directory.glob(pattern)))


def _overlay_counts(project: Project) -> dict[str, int]:
    overlay = project.overlay_path
    return {
        "feedback_records": _line_count(project.root, f"{overlay}/records/feedback", "FB*.md"),
        "failure_records": _line_count(project.root, f"{overlay}/records/failures", "F*.md"),
        "upstream_feedback_records": _line_count(
            project.root,
            f"{overlay}/records/upstream-feedback",
            "UF*.md",
        ),
        "meta_feedback_records": _line_count(
            project.root,
            f"{overlay}/records/meta-feedback",
            "MF*.md",
        ),
        "eval_cases": _line_count(project.root, f"{overlay}/records/eval-cases", "E*.md"),
        "hypotheses": _line_count(project.root, f"{overlay}/records/hypotheses", "H*.md"),
        "decisions": _line_count(project.root, f"{overlay}/records/decisions", "D*.md"),
        "research_scans": _line_count(project.root, f"{overlay}/records/research-scans", "RS*.md"),
        "improvements": _line_count(project.root, f"{overlay}/improvements", "IMP*.md"),
    }


def _pull_first(project: Project, *, pull: bool) -> dict[str, Any]:
    root = project.root
    inside = _git_stdout(root, ["rev-parse", "--is-inside-work-tree"])
    if inside != "true":
        return {
            "is_git_repo": False,
            "branch": None,
            "remote": None,
            "start_sha": None,
            "pulled_sha": None,
            "head_sha": None,
            "pull_status": "no-git",
            "dirty_before_pull": False,
            "status_short": [],
            "can_continue": True,
        }

    branch = _git_stdout(root, ["rev-parse", "--abbrev-ref", "HEAD"])
    upstream = _git_stdout(root, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    start_sha = _git_stdout(root, ["rev-parse", "HEAD"])
    status_lines = _git_status_lines(root)
    dirty = bool(status_lines)
    result: dict[str, Any] = {
        "is_git_repo": True,
        "branch": branch,
        "remote": upstream,
        "start_sha": start_sha,
        "pulled_sha": start_sha,
        "head_sha": start_sha,
        "pull_status": "clean",
        "dirty_before_pull": dirty,
        "status_short": status_lines,
        "ahead": 0,
        "behind": 0,
        "can_continue": True,
    }

    if not pull:
        result["pull_status"] = "not-requested"
        return result

    if dirty:
        result["pull_status"] = "dirty-blocked"
        result["can_continue"] = False
        return result

    if not upstream:
        result["pull_status"] = "no-upstream"
        return result

    fetch = _run_git(root, ["fetch", "--prune"])
    result["fetch"] = {
        "returncode": fetch.returncode,
        "stderr": fetch.stderr.strip(),
    }
    if fetch.returncode != 0:
        result["pull_status"] = "fetch-failed"
        result["can_continue"] = False
        return result

    counts = _ahead_behind(root)
    if counts is not None:
        ahead, behind = counts
        result["ahead"] = ahead
        result["behind"] = behind
    else:
        ahead = behind = 0

    if ahead > 0 and behind > 0:
        result["pull_status"] = "diverged-blocked"
        result["can_continue"] = False
        return result

    if behind > 0:
        pull_result = _run_git(root, ["pull", "--ff-only"])
        result["pull"] = {
            "returncode": pull_result.returncode,
            "stdout": pull_result.stdout.strip(),
            "stderr": pull_result.stderr.strip(),
        }
        if pull_result.returncode != 0:
            result["pull_status"] = "pull-failed"
            result["can_continue"] = False
            return result
        result["pull_status"] = "fast-forwarded"
        pulled_sha = _git_stdout(root, ["rev-parse", "HEAD"])
        result["pulled_sha"] = pulled_sha
        result["head_sha"] = pulled_sha
        return result

    result["pull_status"] = "up-to-date"
    return result


def _lab_health(project: Project) -> dict[str, Any]:
    if project.overlay_mode not in {"upstream-lab", "meta-lab"}:
        return {
            "available": False,
            "reason": f"overlay mode {project.overlay_mode} does not use harness-lab memory",
        }

    lint = lint_lab_memory(project)
    return {
        "available": True,
        "status": lint["status"],
        "reason": lint["reason"],
        "metrics": lint["metrics"],
        "thresholds": lint["thresholds"],
        "pressure": lint["pressure"],
        "triggers": lint["triggers"],
        "snapshot": lint["snapshot"],
        "abstraction": lint["abstraction"],
        "recommended_commands": lint["recommended_commands"] if lint["status"] != "ok" else [],
    }


def _lane_triggers(
    counts: dict[str, int],
    doctor: dict[str, Any],
    migration: dict[str, Any],
    lab_health: dict[str, Any],
) -> dict[str, Any]:
    has_feedback = any(
        counts[key] > 0
        for key in ("feedback_records", "failure_records", "upstream_feedback_records", "meta_feedback_records")
    )
    has_lab_memory = any(counts[key] > 0 for key in ("feedback_records", "research_scans", "improvements"))
    lab_health_triggered = bool(lab_health.get("available") and lab_health.get("status") != "ok")
    if lab_health_triggered:
        lab_reason = "lab health " + str(lab_health.get("status"))
        triggers = lab_health.get("triggers") or []
        if triggers:
            lab_reason += ": " + ", ".join(str(trigger) for trigger in triggers)
    elif has_lab_memory:
        lab_reason = "lab records or dossiers exist"
    else:
        lab_reason = "no local lab records detected"
    has_eval_flow = any(counts[key] > 0 for key in ("eval_cases", "hypotheses"))
    maintainer = bool(doctor.get("warnings") or doctor.get("errors") or not migration.get("ok", True))
    return {
        "issue-triager": {
            "triggered": has_feedback,
            "reason": "feedback records exist" if has_feedback else "no local feedback records detected",
        },
        "maintainer": {
            "triggered": maintainer,
            "reason": "doctor/migration signal present" if maintainer else "doctor/migration clean",
        },
        "open-inventor": {
            "triggered": False,
            "reason": "requires weekly/release/user/cluster trigger outside deterministic preflight",
        },
        "librarian": {
            "triggered": lab_health_triggered or has_lab_memory,
            "reason": lab_reason,
        },
        "critic": {
            "triggered": False,
            "reason": "runs before writes or adopted decisions, not during preflight alone",
        },
        "evaluator": {
            "triggered": has_eval_flow,
            "reason": "eval or hypothesis records exist" if has_eval_flow else "no eval flow records detected",
        },
        "loop-auditor": {
            "triggered": False,
            "reason": "weekly or steward-failure trigger required",
        },
    }


def _subagent_plan(lanes: dict[str, Any]) -> dict[str, Any]:
    return {
        "authorization": "external-prompt-required",
        "spawn_recommendations": [
            {"lane": lane, "status": "recommended", "reason": data["reason"]}
            for lane, data in lanes.items()
            if data["triggered"]
        ],
        "inline_fallback": "Report inline-fallback when subagent tools are unavailable or not authorized.",
    }


def _supervisor_plan(project: Project, *, update_policy: str) -> dict[str, Any]:
    role_summary = {
        "kind": project.data.get("project", {}).get("kind"),
        "profile_id": project.profile_id,
        "overlay_mode": project.overlay_mode,
        "overlay_path": project.overlay_path,
    }
    lanes = []
    for index, lane in enumerate(SUPERVISOR_LANES, start=1):
        lanes.append(
            {
                "order": index,
                **lane,
                "run_policy": "run-unless-fatal-gate-blocks",
                "handoff": (
                    f"Use repo-local skill `.agents/skills/{lane['skill']}/SKILL.md`. "
                    "Use the supervisor preflight JSON, prior lane summaries, runtime authority, "
                    "and project role summary as inputs. Return the lane result contract."
                ),
            }
        )
    return {
        "mode": "sequential-subagents",
        "role_summary": role_summary,
        "update_policy": update_policy,
        "lane_result_contract": LANE_RESULT_CONTRACT,
        "lanes": lanes,
        "rules": [
            "Supervisor does not perform lane work directly.",
            "Wait for each lane result before starting the next lane.",
            "Do not skip a later lane merely because an earlier lane changed files.",
            "Continue past nonfatal blocked lanes and record the blocker.",
            "Use inline fallback one lane at a time when subagents are unavailable.",
        ],
    }


def steward_preflight(
    project: Project,
    *,
    pull: bool,
    check_records: bool = True,
    update_policy: str = "signal-only",
) -> dict[str, Any]:
    if update_policy not in {"signal-only", "apply"}:
        raise ValueError("update_policy must be signal-only or apply")
    git = _pull_first(project, pull=pull)
    if git["can_continue"]:
        doctor = doctor_project(project, check_records=check_records)
        migration = check_migrations(project)
        lab_health = _lab_health(project)
    else:
        doctor = {"ok": None, "errors": [], "warnings": [], "skipped": "pull-first blocked"}
        migration = {"ok": None, "pending": [], "skipped": "pull-first blocked"}
        lab_health = {"available": False, "reason": "pull-first blocked"}
    counts = _overlay_counts(project)
    lanes = _lane_triggers(counts, doctor, migration, lab_health)
    can_continue = bool(git["can_continue"] and doctor.get("ok") is not False and migration.get("ok") is not False)
    return {
        "ok": can_continue,
        "can_continue": can_continue,
        "mode": "pull-first" if pull else "inspect-only",
        "project": {
            "name": project.data.get("project", {}).get("name"),
            "kind": project.data.get("project", {}).get("kind"),
            "profile_id": project.profile_id,
            "overlay_mode": project.overlay_mode,
            "overlay_path": project.overlay_path,
            "root": str(project.root),
        },
        "git": git,
        "doctor": doctor,
        "migration": migration,
        "counts": counts,
        "lab_health": lab_health,
        "lane_triggers": lanes,
        "subagent_plan": _subagent_plan(lanes),
        "supervisor_plan": _supervisor_plan(project, update_policy=update_policy),
        "next_agent_step": (
            "Run the hops-daily-steward supervisor with the generated run ledger."
            if can_continue
            else "Stop before HOPS state changes and ask for human review."
        ),
    }


def steward_run_start(
    project: Project,
    *,
    pull: bool,
    check_records: bool = True,
    update_policy: str = "signal-only",
) -> dict[str, Any]:
    preflight = steward_preflight(
        project,
        pull=pull,
        check_records=check_records,
        update_policy=update_policy,
    )
    now = _now_iso()
    run_id = _new_run_id(project)
    path = _ledger_path(project, run_id)
    supervisor_plan = preflight["supervisor_plan"]
    ledger = {
        "schema_version": "0.1",
        "run_id": run_id,
        "created_at": now,
        "updated_at": now,
        "status": "started" if preflight["can_continue"] else "blocked",
        "project": preflight["project"],
        "git": preflight["git"],
        "preflight": preflight,
        "supervisor_plan": supervisor_plan,
        "lane_result_contract": LANE_RESULT_CONTRACT,
        "lanes": [
            {
                "order": lane["order"],
                "lane": lane["lane"],
                "skill": lane["skill"],
                "status": "pending",
                "result": None,
            }
            for lane in supervisor_plan["lanes"]
        ],
        "events": [
            {
                "at": now,
                "type": "run-start",
                "status": "started" if preflight["can_continue"] else "blocked",
            }
        ],
    }
    _write_json(path, ledger)
    return {
        "ok": preflight["ok"],
        "run_id": run_id,
        "path": _relative_path(project.root, path),
        "preflight": preflight,
        "supervisor_plan": supervisor_plan,
        "ledger": ledger,
    }


def validate_lane_result(result: Any) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(result, dict):
        return {
            "ok": False,
            "errors": ["lane result must be a JSON object"],
            "required_fields": LANE_RESULT_CONTRACT,
        }

    for field in LANE_RESULT_CONTRACT:
        if field not in result:
            errors.append(f"missing required field: {field}")

    status = result.get("status")
    if status not in LANE_RESULT_STATUSES:
        errors.append(
            "status must be one of: " + ", ".join(sorted(LANE_RESULT_STATUSES))
        )

    for field in ("changed_files", "records_created_or_updated", "issues_touched"):
        if field in result and not isinstance(result[field], list):
            errors.append(f"{field} must be a list")

    if "stop_reason" in result and result["stop_reason"] is not None and not isinstance(result["stop_reason"], str):
        errors.append("stop_reason must be a string or null")

    return {
        "ok": not errors,
        "errors": errors,
        "required_fields": LANE_RESULT_CONTRACT,
        "allowed_statuses": sorted(LANE_RESULT_STATUSES),
        "result": result,
    }


def steward_record_lane_result(
    project: Project,
    *,
    run_id: str,
    lane: str,
    result: dict[str, Any],
) -> dict[str, Any]:
    validation = validate_lane_result(result)
    if not validation["ok"]:
        return {"ok": False, "run_id": run_id, "lane": lane, "validation": validation}

    path, ledger = _read_ledger(project, run_id)
    lane_entries = ledger.get("lanes")
    if not isinstance(lane_entries, list):
        raise ValueError("steward run ledger has no lanes list")
    selected = None
    for entry in lane_entries:
        if isinstance(entry, dict) and lane in {entry.get("lane"), entry.get("skill")}:
            selected = entry
            break
    if selected is None:
        known = [
            str(entry.get("lane"))
            for entry in lane_entries
            if isinstance(entry, dict) and entry.get("lane")
        ]
        return {
            "ok": False,
            "run_id": run_id,
            "lane": lane,
            "error": "unknown lane",
            "known_lanes": known,
        }

    now = _now_iso()
    selected["status"] = result["status"]
    selected["result"] = result
    selected["updated_at"] = now
    ledger["updated_at"] = now
    ledger.setdefault("events", []).append(
        {
            "at": now,
            "type": "lane-result",
            "lane": selected.get("lane"),
            "skill": selected.get("skill"),
            "status": result["status"],
        }
    )
    _write_json(path, ledger)
    return {
        "ok": True,
        "run_id": run_id,
        "path": _relative_path(project.root, path),
        "lane": selected.get("lane"),
        "skill": selected.get("skill"),
        "status": result["status"],
        "ledger": ledger,
    }


def steward_run_end(project: Project, *, run_id: str, status: str) -> dict[str, Any]:
    if status not in RUN_END_STATUSES:
        raise ValueError("status must be one of: " + ", ".join(sorted(RUN_END_STATUSES)))

    path, ledger = _read_ledger(project, run_id)
    ledger_lanes = ledger.get("lanes")
    lanes: list[Any] = ledger_lanes if isinstance(ledger_lanes, list) else []
    pending = [
        lane.get("lane")
        for lane in lanes
        if isinstance(lane, dict) and lane.get("status") == "pending"
    ]
    if status == "completed" and pending:
        return {
            "ok": False,
            "run_id": run_id,
            "status": status,
            "error": "cannot complete run with pending lanes",
            "pending_lanes": pending,
        }

    now = _now_iso()
    ledger["status"] = status
    ledger["updated_at"] = now
    ledger["completed_at"] = now
    ledger.setdefault("events", []).append({"at": now, "type": "run-end", "status": status})
    _write_json(path, ledger)
    return {
        "ok": True,
        "run_id": run_id,
        "path": _relative_path(project.root, path),
        "status": status,
        "pending_lanes": pending,
        "ledger": ledger,
    }


def steward_finalize(
    project: Project,
    *,
    policy: str,
    validation_passed: bool = False,
    branch: str | None = None,
    branch_prefix: str = "codex/steward",
    message: str = "hops daily steward local advance",
) -> dict[str, Any]:
    if policy not in {"patch-only", "commit-local"}:
        raise ValueError("policy must be patch-only or commit-local")

    root = project.root
    inside = _git_stdout(root, ["rev-parse", "--is-inside-work-tree"])
    if inside != "true":
        return {
            "ok": False,
            "policy": policy,
            "error": "not a git repository",
            "can_continue_next_run": False,
        }

    branch_before = _git_stdout(root, ["rev-parse", "--abbrev-ref", "HEAD"])
    head_before = _git_stdout(root, ["rev-parse", "HEAD"])
    status_before = _git_status_lines(root)
    result: dict[str, Any] = {
        "ok": True,
        "policy": policy,
        "branch_before": branch_before,
        "branch_after": branch_before,
        "head_before": head_before,
        "head_after": head_before,
        "commit_hash": None,
        "changed_files": status_before,
        "validation_passed": validation_passed,
        "pushed": False,
        "can_continue_next_run": not status_before,
    }

    if not status_before:
        result["status"] = "no-changes"
        return result

    if policy == "patch-only":
        result["status"] = "patch-left-in-worktree"
        result["can_continue_next_run"] = False
        result["next"] = "Review, commit, or discard the patch before the next scheduled preflight."
        return result

    if not validation_passed:
        result["ok"] = False
        result["status"] = "validation-required"
        result["can_continue_next_run"] = False
        result["next"] = "Run validation before commit-local finalize."
        return result

    target_branch = branch
    if not target_branch:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        short_sha = (head_before or "unknown")[:7]
        target_branch = f"{branch_prefix}/{timestamp}-{short_sha}"
    if branch_before != target_branch:
        _git_required(root, ["switch", "-c", target_branch])

    _git_required(root, ["add", "-A"])
    _git_required(root, ["commit", "-m", message])
    head_after = _git_required(root, ["rev-parse", "HEAD"])
    status_after = _git_status_lines(root)
    result.update(
        {
            "status": "committed",
            "branch_after": target_branch,
            "head_after": head_after,
            "commit_hash": head_after,
            "changed_files_after": status_after,
            "can_continue_next_run": not status_after,
        }
    )
    return result
