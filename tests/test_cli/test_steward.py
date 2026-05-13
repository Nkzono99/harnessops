import json
import subprocess

from typer.testing import CliRunner

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
    assert payload["git"]["pull_status"] in {"no-git", "not-requested"}
    assert "issue-triager" in payload["lane_triggers"]
    assert payload["subagent_plan"]["authorization"] == "external-prompt-required"
    assert "Run hops-daily-steward lanes" in payload["next_agent_step"]


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
