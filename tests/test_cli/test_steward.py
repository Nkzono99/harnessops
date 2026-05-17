import json
import subprocess

from typer.testing import CliRunner

from harnessops.core import steward as steward_core
from harnessops.cli.main import app


runner = CliRunner()


def run_cli(args):
    result = runner.invoke(app, args)
    assert result.exit_code == 0, result.output
    return result


def run_git(root, args):
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)


def test_steward_preflight_json_reports_run_ledger(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])

    result = run_cli(["steward", "preflight", "--json"])
    payload = json.loads(result.output)

    assert payload["ok"] is True
    assert payload["mode"] == "inspect-only"
    assert payload["project"]["profile_id"] == "harnessops-core"
    assert payload["lab_health"]["available"] is True
    assert payload["git"]["pull_status"] in {"no-git", "not-requested"}
    assert "issue-triager" in payload["lane_triggers"]
    assert payload["lane_triggers"]["open-meta-scan"]["triggered"] is True
    assert payload["subagent_plan"]["authorization"] == "external-prompt-required"
    assert "open-meta-scan" in {
        item["lane"] for item in payload["subagent_plan"]["spawn_recommendations"]
    }
    plan = payload["supervisor_plan"]
    assert plan["mode"] == "sequential-subagents"
    assert plan["update_policy"] == "signal-only"
    assert plan["lane_result_contract"] == [
        "status",
        "changed_files",
        "records_created_or_updated",
        "issues_touched",
        "validation",
        "recommended_next",
        "stop_reason",
    ]
    assert [lane["skill"] for lane in plan["lanes"]] == [
        "hops-maintenance-steward",
        "hops-issue-execution-steward",
        "hops-open-meta-scan",
        "hops-invention-steward",
        "hops-priority-improvement-steward",
        "hops-finalize-steward",
    ]
    open_meta_lane = plan["lanes"][2]
    assert open_meta_lane["lane"] == "open-meta-scan"
    assert "Raw Ideas" in open_meta_lane["handoff"]
    assert "changed_files" in open_meta_lane["handoff"]
    assert "Return the lane result contract" in plan["lanes"][0]["handoff"]
    assert "Run the hops-daily-steward supervisor" in payload["next_agent_step"]


def test_steward_preflight_accepts_update_policy_apply(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])

    result = run_cli(["steward", "preflight", "--json", "--update-policy", "apply"])
    payload = json.loads(result.output)

    assert payload["supervisor_plan"]["update_policy"] == "apply"


def test_steward_preflight_rejects_unknown_update_policy(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])

    result = runner.invoke(app, ["steward", "preflight", "--json", "--update-policy", "always"])

    assert result.exit_code == 1
    assert "update_policy must be signal-only or apply" in result.output


def _valid_lane_result(status: str = "completed") -> dict:
    return {
        "status": status,
        "changed_files": [],
        "records_created_or_updated": [],
        "issues_touched": [],
        "validation": "ok",
        "recommended_next": [],
        "stop_reason": None,
    }


def test_steward_run_start_writes_ledger(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])

    result = run_cli(["steward", "run", "start", "--json", "--update-policy", "apply"])
    payload = json.loads(result.output)
    ledger_path = root / payload["path"]

    assert payload["ok"] is True
    assert payload["supervisor_plan"]["update_policy"] == "apply"
    assert ledger_path.exists()
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    assert ledger["run_id"] == payload["run_id"]
    assert [lane["status"] for lane in ledger["lanes"]] == ["pending"] * 6


def test_steward_run_validates_lane_result_json(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])

    valid = json.dumps(_valid_lane_result())
    result = run_cli(
        ["steward", "run", "validate-lane-result", "--result-json", valid, "--json"]
    )
    payload = json.loads(result.output)
    assert payload["ok"] is True

    invalid = json.dumps({"status": "done"})
    result = runner.invoke(
        app,
        ["steward", "run", "validate-lane-result", "--result-json", invalid, "--json"],
    )
    payload = json.loads(result.output)
    assert result.exit_code == 1
    assert payload["ok"] is False
    assert "missing required field: changed_files" in payload["errors"]


def test_steward_run_records_lane_result_and_end_status(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])

    started = json.loads(run_cli(["steward", "run", "start", "--json"]).output)
    run_id = started["run_id"]
    result_json = json.dumps(_valid_lane_result("completed"))
    recorded = run_cli(
        [
            "steward",
            "run",
            "record-lane-result",
            "--run-id",
            run_id,
            "--lane",
            "maintenance",
            "--result-json",
            result_json,
            "--json",
        ]
    )
    payload = json.loads(recorded.output)
    assert payload["ok"] is True
    assert payload["status"] == "completed"

    ledger = json.loads((root / started["path"]).read_text(encoding="utf-8"))
    assert ledger["lanes"][0]["status"] == "completed"
    assert ledger["events"][-1]["type"] == "lane-result"

    completed = runner.invoke(
        app,
        ["steward", "run", "end", "--run-id", run_id, "--status", "completed", "--json"],
    )
    assert completed.exit_code == 1
    assert "cannot complete run with pending lanes" in completed.output

    ended = run_cli(
        ["steward", "run", "end", "--run-id", run_id, "--status", "blocked", "--json"]
    )
    payload = json.loads(ended.output)
    assert payload["ok"] is True
    assert payload["status"] == "blocked"


def test_steward_preflight_routes_stale_lab_health_to_librarian(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])

    def fake_lint_lab_memory(_project):
        return {
            "status": "needs-abstraction",
            "reason": "triggers-present",
            "metrics": {"file_count": 300, "byte_count": 10, "improvement_count": 1},
            "thresholds": {"max_files": 256, "max_bytes": 2000000, "max_improvements": 50},
            "pressure": ["file_count>256"],
            "triggers": ["file_count>256", "semantic_memory_stale"],
            "snapshot": {"path": "harness-lab/knowledge/lab-memory.yml", "stale": False},
            "abstraction": {"path": "harness-lab/knowledge/lab-memory-abstraction.yml", "stale": True},
            "recommended_commands": [
                "hops lab memory compact --force",
                "hops lab memory prepare --force",
                "Use the hops-compact-lab-memory skill to update abstract knowledge.",
            ],
        }

    monkeypatch.setattr(steward_core, "lint_lab_memory", fake_lint_lab_memory)

    result = run_cli(["steward", "preflight", "--json"])
    payload = json.loads(result.output)

    assert payload["lab_health"]["status"] == "needs-abstraction"
    assert payload["lab_health"]["triggers"] == ["file_count>256", "semantic_memory_stale"]
    assert payload["lab_health"]["recommended_commands"][1] == "hops lab memory prepare --force"
    assert payload["lane_triggers"]["librarian"]["triggered"] is True
    assert payload["lane_triggers"]["librarian"]["reason"] == (
        "lab health needs-abstraction: file_count>256, semantic_memory_stale"
    )


def test_steward_preflight_skips_lab_health_for_project_repos(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project"])

    result = run_cli(["steward", "preflight", "--json"])
    payload = json.loads(result.output)

    assert payload["project"]["overlay_mode"] == "feedback-source"
    assert payload["lab_health"]["available"] is False
    assert "does not use harness-lab memory" in payload["lab_health"]["reason"]


def test_steward_preflight_pull_blocks_dirty_worktree(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_git(root, ["init"])
    run_git(root, ["config", "user.email", "test@example.com"])
    run_git(root, ["config", "user.name", "HarnessOps Test"])
    run_cli(["init", "--profile", "harnessops-core"])
    run_git(root, ["add", "."])
    run_git(root, ["commit", "-m", "baseline"])
    (root / "README.md").write_text("# dirty\n", encoding="utf-8")

    result = runner.invoke(app, ["steward", "preflight", "--pull", "--json"])
    payload = json.loads(result.output)

    assert result.exit_code == 1
    assert payload["ok"] is False
    assert payload["git"]["pull_status"] == "dirty-blocked"
    assert payload["git"]["dirty_before_pull"] is True
    assert payload["doctor"]["skipped"] == "pull-first blocked"
    assert "Stop before HOPS state changes" in payload["next_agent_step"]


def test_steward_finalize_patch_only_leaves_worktree_dirty(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_git(root, ["init"])
    run_git(root, ["config", "user.email", "test@example.com"])
    run_git(root, ["config", "user.name", "HarnessOps Test"])
    run_cli(["init", "--profile", "harnessops-core"])
    run_git(root, ["add", "."])
    run_git(root, ["commit", "-m", "baseline"])
    (root / "README.md").write_text("# patch\n", encoding="utf-8")

    result = run_cli(["steward", "finalize", "--policy", "patch-only", "--json"])
    payload = json.loads(result.output)

    assert payload["ok"] is True
    assert payload["status"] == "patch-left-in-worktree"
    assert payload["commit_hash"] is None
    assert payload["can_continue_next_run"] is False
    assert run_git(root, ["status", "--porcelain"]).stdout.strip()


def test_steward_finalize_commit_local_requires_validation(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_git(root, ["init"])
    run_git(root, ["config", "user.email", "test@example.com"])
    run_git(root, ["config", "user.name", "HarnessOps Test"])
    run_cli(["init", "--profile", "harnessops-core"])
    run_git(root, ["add", "."])
    run_git(root, ["commit", "-m", "baseline"])
    branch_before = run_git(root, ["rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
    (root / "README.md").write_text("# needs validation\n", encoding="utf-8")

    result = runner.invoke(app, ["steward", "finalize", "--policy", "commit-local", "--json"])
    payload = json.loads(result.output)

    assert result.exit_code == 1
    assert payload["ok"] is False
    assert payload["status"] == "validation-required"
    assert run_git(root, ["rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip() == branch_before


def test_steward_finalize_commit_local_creates_local_branch_and_commit(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_git(root, ["init"])
    run_git(root, ["config", "user.email", "test@example.com"])
    run_git(root, ["config", "user.name", "HarnessOps Test"])
    run_cli(["init", "--profile", "harnessops-core"])
    run_git(root, ["add", "."])
    run_git(root, ["commit", "-m", "baseline"])
    (root / "README.md").write_text("# committed\n", encoding="utf-8")

    result = run_cli(
        [
            "steward",
            "finalize",
            "--policy",
            "commit-local",
            "--validation-passed",
            "--branch",
            "codex/steward/test-run",
            "--message",
            "daily steward test commit",
            "--json",
        ]
    )
    payload = json.loads(result.output)

    assert payload["ok"] is True
    assert payload["status"] == "committed"
    assert payload["branch_after"] == "codex/steward/test-run"
    assert payload["commit_hash"]
    assert payload["pushed"] is False
    assert payload["can_continue_next_run"] is True
    assert run_git(root, ["status", "--porcelain"]).stdout.strip() == ""
    assert run_git(root, ["log", "-1", "--pretty=%s"]).stdout.strip() == "daily steward test commit"
