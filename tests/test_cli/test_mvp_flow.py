import datetime as dt
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from harnessops import __version__
from typer.testing import CliRunner

from harnessops.cli import feedback as feedback_cli
from harnessops.cli import update_notice
from harnessops.core import upgrade_chain
from harnessops.cli.main import app
from harnessops.core import yamlio
from harnessops.core.agent_bridge import packaged_bridge_files
from harnessops.core.lock import sha256_file
from harnessops.core.project import load_project
from harnessops.core.records import create_or_update_improvement_dossier, dump_record, read_record


runner = CliRunner()


def run_cli(args):
    result = runner.invoke(app, args)
    assert result.exit_code == 0, result.output
    return result


def test_init_doctor_migrate_project(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)

    run_cli(["init"])
    assert (root / ".harnessops/project.toml").exists()
    project_toml = tomllib.loads((root / ".harnessops/project.toml").read_text(encoding="utf-8"))
    assert project_toml["github_flow"]["enabled"] is False
    assert (root / ".harnessops/lock.json").exists()
    assert (root / "harness-feedback/README.md").exists()
    assert (root / "harness-feedback/records/failures").is_dir()
    gitignore = (root / ".gitignore").read_text(encoding="utf-8")
    assert "# BEGIN harnessops" in gitignore
    assert ".harnessops/cache/*" in gitignore
    assert "!.harnessops/cache/.gitkeep" in gitignore
    assert ".harnessops/tmp/" in gitignore

    run_cli(["doctor", "--check-overlay", "--check-records"])
    run_cli(["migrate", "--check"])


def test_init_doctor_migrate_upstream(copy_fixture, monkeypatch):
    root = copy_fixture("runops-upstream-minimal")
    monkeypatch.chdir(root)

    run_cli(["init", "--profile", "runops-upstream"])
    project_toml = tomllib.loads((root / ".harnessops/project.toml").read_text(encoding="utf-8"))
    assert project_toml["github_flow"]["enabled"] is True
    assert (root / "harness-lab/README.md").exists()
    assert (root / "harness-lab/records/feedback").is_dir()
    run_cli(["doctor", "--check-overlay", "--check-records"])
    run_cli(["migrate", "--check"])


def test_paper_harness_upstream_manifest_uses_pops(copy_fixture, monkeypatch):
    root = copy_fixture("paper-harness-upstream-minimal")
    monkeypatch.chdir(root)

    run_cli(["init", "--profile", "paper-harness-upstream"])

    manifest = tomllib.loads((root / ".harness/manifest.toml").read_text(encoding="utf-8"))
    assert manifest["commands"] == {
        "doctor": "pops doctor",
        "update": "pops update-harness",
        "migrate": "pops migrate",
        "feedback": "pops feedback",
        "version": "pops version",
    }


def test_failure_route_export_import_eval_hypothesis_decision(copy_fixture, tmp_path, monkeypatch):
    project_root = copy_fixture("paper-project-minimal")
    monkeypatch.chdir(project_root)
    run_cli(["init", "--profile", "paper-harness-project"])
    add = run_cli(
        [
            "add-failure",
            "--title",
            "Local term leaked into manuscript",
            "--target",
            "paper-harness",
            "--context",
            f"Manuscript used private term from {project_root}/refs/private/source.md",
            "--what-happened",
            "public terminology check missed internal wording",
            "--desired-behavior",
            "paper-harness should detect private terms",
        ]
    )
    failure_path = project_root / add.output.strip()
    frontmatter, _ = read_record(failure_path)
    assert frontmatter["record_type"] == "failure"
    assert frontmatter["id"] == "F0001"

    route = run_cli(["route", "--record", "F0001", "--json"])
    assert "target-upstream-candidate" in route.output

    feedback_draft = run_cli(["add-feedback", "--from", "F0001", "--summary", "Terminology feedback draft"])
    feedback_path = project_root / feedback_draft.output.strip()
    feedback_frontmatter, feedback_body = read_record(feedback_path)
    assert feedback_frontmatter["record_type"] == "upstream_feedback"
    assert feedback_frontmatter["source_failure"] == "F0001"
    assert "TODO" not in feedback_body

    export = run_cli(["feedback", "export", "--sanitize"])
    bundle = project_root / export.output.strip()
    bundle_text = bundle.read_text(encoding="utf-8")
    assert str(project_root) not in bundle_text
    assert "非公開情報を除外" in bundle_text

    lab_root = tmp_path / "paper-upstream"
    lab_root.mkdir()
    monkeypatch.chdir(lab_root)
    run_cli(["init", "--profile", "paper-harness-upstream"])
    imported = run_cli(["feedback", "import", str(bundle)])
    imported_path = lab_root / imported.output.strip()
    imported_frontmatter, _ = read_record(imported_path)
    assert imported_frontmatter["record_type"] == "imported_feedback"
    assert imported_frontmatter["id"] == "FB0001"

    eval_case = run_cli(["lab", "new-eval-case", "--from", "FB0001"])
    assert (lab_root / eval_case.output.strip()).exists()
    hypothesis = run_cli(["propose", "--from", "E0001"])
    assert "records/hypotheses/H0001" in hypothesis.output
    hypothesis_frontmatter, hypothesis_body = read_record(lab_root / hypothesis.output.strip())
    assert hypothesis_frontmatter["record_type"] == "hypothesis"
    assert "中止基準" in hypothesis_body
    assert "TODO" not in hypothesis_body
    eval_result = run_cli(
        [
            "eval",
            "--case",
            "E0001",
            "--manual",
            "--score",
            "impact=4",
            "--score",
            "anti-theater=5",
            "--notes",
            "Manual evidence recorded.",
        ]
    )
    assert "eval-results/E0001-manual-score.yml" in eval_result.output
    decision = run_cli(["decide", "--from", "H0001", "--status", "parked"])
    assert "records/decisions/D0001" in decision.output

    adopted = run_cli(
        [
            "decide",
            "--from",
            "H0001",
            "--status",
            "adopted",
            "--reason",
            "Eval case passed with a smaller change.",
            "--evidence",
            "See harness-lab/views/eval-results/E0001-manual-score.yml",
            "--regression-risk",
            "Low risk after manual scorecard review.",
            "--guard-path",
            "tests/test_cli/test_mvp_flow.py",
        ]
    )
    assert "records/decisions/D0002" in adopted.output


def test_agent_bridge_generation(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project", "--with-agent-bridge"])
    skill = root / ".agents/skills/harnessops-bridge/SKILL.md"
    assert skill.exists()
    text = skill.read_text(encoding="utf-8")
    assert "hops doctor" in text
    assert "feedback-source interface" in text
    assert "hops feedback export --sanitize" in text
    assert "uvx --from harnessops hops lab capture" not in text
    assert "uvx --from harnessops hops propose" not in text
    assert "直接組み替えない" in text
    assert (root / ".agents/skills/hops-add-failure/SKILL.md").exists()
    assert not (root / ".agents/skills/hops-github-flow/SKILL.md").exists()
    assert not (root / ".agents/skills/hops-issue-triage/SKILL.md").exists()
    assert not (root / ".agents/skills/hops-run-lab/SKILL.md").exists()
    assert (root / ".agents/skills/hops-update-harness/SKILL.md").exists()


def test_agent_bridge_generation_for_lab_repo_includes_lab_interface(copy_fixture, monkeypatch):
    root = copy_fixture("runops-upstream-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-upstream", "--with-agent-bridge"])
    skill = root / ".agents/skills/harnessops-bridge/SKILL.md"
    text = skill.read_text(encoding="utf-8")
    assert "hops feedback import <bundle-path>" in text
    assert "hops lab capture" in text
    assert "hops propose" in text
    assert "hops github-flow preflight" in text
    assert (root / ".agents/skills/hops-github-flow/SKILL.md").exists()
    assert (root / ".agents/skills/hops-issue-triage/SKILL.md").exists()
    assert (root / ".agents/skills/hops-run-lab/SKILL.md").exists()
    assert (root / ".agents/skills/hops-update-harness/SKILL.md").exists()


def test_doctor_warns_about_stale_editable_bridge_fallback(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project", "--with-agent-bridge"])
    bridge = root / ".agents/skills/harnessops-bridge/SKILL.md"
    bridge.write_text(
        bridge.read_text(encoding="utf-8").replace(
            "uvx --from harnessops hops <command>",
            "uv run --with-editable . hops <command>",
        ),
        encoding="utf-8",
    )

    doctor = run_cli(["doctor", "--check-overlay"])

    assert "agent bridge fallback may be invalid for this repo" in doctor.output
    assert ".agents/skills/harnessops-bridge/SKILL.md" in doctor.output
    assert "uvx --refresh-package harnessops --from harnessops hops update-harness --agent-bridge" in doctor.output


def test_doctor_allows_editable_bridge_fallback_when_repo_provides_hops(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project", "--with-agent-bridge"])
    (root / "pyproject.toml").write_text(
        "[project]\nname = \"local-hops-provider\"\nversion = \"0.1.0\"\n\n"
        "[project.scripts]\nhops = \"local_hops:main\"\n",
        encoding="utf-8",
    )
    bridge = root / ".agents/skills/harnessops-bridge/SKILL.md"
    bridge.write_text(
        bridge.read_text(encoding="utf-8").replace(
            "uvx --from harnessops hops <command>",
            "uv run --with-editable . hops <command>",
        ),
        encoding="utf-8",
    )

    doctor = run_cli(["doctor", "--check-overlay"])

    assert "agent bridge fallback may be invalid for this repo" not in doctor.output


def test_update_harness_preserves_edited_managed_file_as_new(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project"])
    readme = root / "harness-feedback/README.md"
    readme.write_text("# Custom feedback notes\n", encoding="utf-8")

    result = run_cli(["update-harness"])

    assert ".new" in result.output
    assert readme.read_text(encoding="utf-8") == "# Custom feedback notes\n"
    assert (root / "harness-feedback/README.md.new").exists()


def test_update_harness_force_overwrites_edited_managed_file(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project"])
    readme = root / "harness-feedback/README.md"
    readme.write_text("# Custom feedback notes\n", encoding="utf-8")

    run_cli(["update-harness", "--force"])

    assert "harness-feedback" in readme.read_text(encoding="utf-8")
    assert not (root / "harness-feedback/README.md.new").exists()


def test_update_harness_recreates_missing_lock(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project"])
    (root / ".harnessops/lock.json").unlink()

    run_cli(["update-harness"])

    lock = json.loads((root / ".harnessops/lock.json").read_text(encoding="utf-8"))
    assert lock["overlay"] == {"mode": "feedback-source", "path": "harness-feedback"}
    assert "harness-feedback/README.md" in lock["managed_files"]


def test_update_harness_repairs_harnessops_gitignore_block(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project"])
    gitignore_path = root / ".gitignore"
    gitignore_path.write_text("dist/\n.harnessops/cache/*\n!.harnessops/cache/.gitkeep\n", encoding="utf-8")

    result = run_cli(["update-harness"])

    gitignore = gitignore_path.read_text(encoding="utf-8")
    assert "gitignore: updated .gitignore" in result.output
    assert "dist/" in gitignore
    assert gitignore.count(".harnessops/cache/*") == 1
    assert gitignore.count("!.harnessops/cache/.gitkeep") == 1
    assert "# BEGIN harnessops" in gitignore
    assert "# END harnessops" in gitignore
    assert ".harnessops/tmp/" in gitignore


def test_update_harness_can_add_repo_local_agent_bridge(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project"])

    run_cli(["update-harness", "--agent-bridge", "--codex"])

    assert (root / ".agents/skills/harnessops-bridge/SKILL.md").exists()
    assert (root / ".agents/skills/hops-add-failure/SKILL.md").exists()
    assert not (root / ".agents/skills/hops-github-flow/SKILL.md").exists()
    assert not (root / ".agents/skills/hops-run-lab/SKILL.md").exists()
    assert (root / ".agents/skills/hops-update-harness/SKILL.md").exists()


def test_update_harness_retires_project_side_lab_agent_skills(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project", "--with-agent-bridge"])
    stale = root / ".agents/skills/hops-run-lab/SKILL.md"
    stale.parent.mkdir(parents=True)
    stale.write_text("# old generated lab skill\n", encoding="utf-8")
    rel = stale.relative_to(root).as_posix()
    lock_path = root / ".harnessops/lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["agent_bridge"]["managed_files"][rel] = sha256_file(stale)
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result = run_cli(["update-harness", "--agent-bridge", "--codex"])

    assert "agent bridge: retired 1" in result.output
    assert not stale.exists()
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    assert rel not in lock["agent_bridge"]["managed_files"]


def test_init_can_disable_github_flow_for_target_repo(copy_fixture, monkeypatch):
    root = copy_fixture("runops-upstream-minimal")
    monkeypatch.chdir(root)

    run_cli(["init", "--profile", "runops-upstream", "--with-agent-bridge", "--no-github-flow"])

    project_toml = tomllib.loads((root / ".harnessops/project.toml").read_text(encoding="utf-8"))
    assert project_toml["github_flow"]["enabled"] is False
    assert not (root / ".agents/skills/hops-github-flow/SKILL.md").exists()


def test_agent_bridge_can_disable_github_flow_for_target_repo(copy_fixture, monkeypatch):
    root = copy_fixture("runops-upstream-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-upstream"])

    run_cli(["agent", "bridge", "--codex", "--no-github-flow"])

    assert (root / ".agents/skills/harnessops-bridge/SKILL.md").exists()
    assert not (root / ".agents/skills/hops-github-flow/SKILL.md").exists()


def test_update_harness_retires_disabled_github_flow_skill(copy_fixture, monkeypatch):
    root = copy_fixture("runops-upstream-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-upstream", "--with-agent-bridge"])
    skill = root / ".agents/skills/hops-github-flow/SKILL.md"
    assert skill.exists()
    project_path = root / ".harnessops/project.toml"
    project_path.write_text(
        project_path.read_text(encoding="utf-8").replace("enabled = true", "enabled = false"),
        encoding="utf-8",
    )

    result = run_cli(["update-harness", "--agent-bridge", "--codex"])

    assert "agent bridge: retired 1" in result.output
    assert not skill.exists()


def test_github_flow_cli_stops_in_project_repo(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project"])

    result = runner.invoke(app, ["github-flow", "preflight", "--json"])

    assert result.exit_code == 1
    payload = json.loads(result.output)
    assert payload["ok"] is False
    assert "not a target/meta harness repository" in payload["reason"]


def test_github_flow_publish_requires_validation(copy_fixture, monkeypatch):
    root = copy_fixture("runops-upstream-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-upstream"])

    result = runner.invoke(app, ["github-flow", "publish", "--json"])

    assert result.exit_code == 1
    payload = json.loads(result.output)
    assert payload["ok"] is False
    assert payload["reason"] == "--validation-passed is required"


def test_update_harness_refreshes_unmodified_stale_agent_bridge(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project", "--with-agent-bridge"])
    skill = root / ".agents/skills/hops-update-harness/SKILL.md"
    stale_text = skill.read_text(encoding="utf-8").replace("hops update-harness", "hops update-harness-old", 1)
    skill.write_text(stale_text, encoding="utf-8")
    rel = skill.relative_to(root).as_posix()
    lock_path = root / ".harnessops/lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["agent_bridge"]["managed_files"][rel] = sha256_file(skill)
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result = run_cli(["update-harness", "--agent-bridge", "--codex"])

    assert "agent bridge: updated" in result.output
    assert skill.read_text(encoding="utf-8") == packaged_bridge_files(root, codex=True)[skill]


def test_update_harness_preserves_edited_agent_bridge_file_as_new(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project", "--with-agent-bridge"])
    skill = root / ".agents/skills/hops-update-harness/SKILL.md"
    skill.write_text("# Local bridge edit\n", encoding="utf-8")

    result = run_cli(["update-harness", "--agent-bridge", "--codex"])

    assert "agent bridge: conflicted 1" in result.output
    assert "SKILL.md.new" in result.output
    assert skill.read_text(encoding="utf-8") == "# Local bridge edit\n"
    assert skill.with_name("SKILL.md.new").read_text(encoding="utf-8") == packaged_bridge_files(root, codex=True)[skill]


def test_update_harness_force_overwrites_edited_agent_bridge_file(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project", "--with-agent-bridge"])
    skill = root / ".agents/skills/hops-update-harness/SKILL.md"
    skill.write_text("# Local bridge edit\n", encoding="utf-8")

    run_cli(["update-harness", "--agent-bridge", "--codex", "--force-agent-bridge"])

    assert skill.read_text(encoding="utf-8") == packaged_bridge_files(root, codex=True)[skill]
    assert not skill.with_name("SKILL.md.new").exists()


def test_update_harness_plan_upgrade_reports_minor_checkpoints(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project"])
    lock_path = root / ".harnessops/lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["harnessops_version"] = "0.0.1"
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    monkeypatch.setattr(
        upgrade_chain,
        "fetch_pypi_versions",
        lambda: (["0.0.3", "0.0.5", "0.1.6"], "0.1.6"),
    )

    result = run_cli(["update-harness", "--plan-upgrade"])

    assert "upgrade chain: needed" in result.output
    assert "0.0.5" in result.output
    assert __version__ in result.output
    assert "uvx --from harnessops==0.0.5 hops update-harness" in result.output


def test_update_harness_apply_upgrade_chain_runs_exact_uvx_steps(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project"])
    lock_path = root / ".harnessops/lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["harnessops_version"] = "0.0.1"
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    monkeypatch.setattr(
        upgrade_chain,
        "fetch_pypi_versions",
        lambda: (["0.0.5", "0.1.6"], "0.1.6"),
    )
    calls = []

    def fake_run_step(step, *, cwd):
        calls.append((step.version, step.command, cwd))
        return upgrade_chain.UpgradeRun(
            version=step.version,
            command=step.command,
            returncode=0,
            stdout=f"updated {step.version}\n",
            stderr="",
        )

    monkeypatch.setattr(upgrade_chain, "run_upgrade_step", fake_run_step)

    result = run_cli(["update-harness", "--apply-upgrade-chain", "--agent-bridge", "--codex"])

    assert [call[0] for call in calls] == ["0.0.5", __version__]
    assert calls[0][1][:4] == ["uvx", "--from", "harnessops==0.0.5", "hops"]
    assert "--agent-bridge" not in calls[0][1]
    assert calls[-1][1][-2:] == ["--agent-bridge", "--codex"]
    assert "upgrade chain: 0.0.5 ok" in result.output
    assert "upgrade chain: " + __version__ + " ok" in result.output


def test_update_harness_auto_chains_intermediate_steps_before_current_refresh(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project"])
    lock_path = root / ".harnessops/lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["harnessops_version"] = "0.0.1"
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    monkeypatch.setattr(
        upgrade_chain,
        "fetch_pypi_versions",
        lambda: (["0.0.5", "0.1.6"], "0.1.6"),
    )
    calls = []

    def fake_run_step(step, *, cwd):
        calls.append(step.version)
        return upgrade_chain.UpgradeRun(
            version=step.version,
            command=step.command,
            returncode=0,
            stdout="",
            stderr="",
        )

    monkeypatch.setattr(upgrade_chain, "run_upgrade_step", fake_run_step)

    result = run_cli(["update-harness"])

    assert calls == ["0.0.5"]
    assert "upgrade chain: 0.0.5 ok" in result.output
    updated_lock = json.loads(lock_path.read_text(encoding="utf-8"))
    assert updated_lock["harnessops_version"] == __version__


def test_hops_usage_notices_stale_harnessops_lock_once(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)

    run_cli(["init", "--profile", "runops-project"])
    lock_path = root / ".harnessops" / "lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["harnessops_version"] = "0.0.1"
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    first = run_cli(["doctor"])
    assert "HarnessOps update path available" in first.stderr
    assert "repo managed artifacts: 0.0.1" in first.stderr
    assert "current hops runtime:" in first.stderr
    assert "latest PyPI release:    unknown" in first.stderr
    assert "uvx --refresh-package harnessops --from harnessops hops update-harness --agent-bridge" in first.stderr
    assert "uvx --from harnessops hops doctor --check-overlay --check-records" in first.stderr
    assert "uvx --from harnessops hops migrate --check" in first.stderr

    cache_path = root / ".harnessops" / "cache" / "update-notice.json"
    assert cache_path.exists()

    second = run_cli(["doctor"])
    assert "HarnessOps update path available" not in second.stderr


def test_hops_usage_notices_when_current_runtime_is_behind_pypi(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    monkeypatch.delenv("HOPS_DISABLE_PYPI_UPDATE_CHECK", raising=False)
    monkeypatch.setattr(update_notice, "_fetch_latest_pypi_version", lambda: "99.0.0")

    run_cli(["init", "--profile", "runops-project"])
    lock_path = root / ".harnessops" / "lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["harnessops_version"] = __version__
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    first = run_cli(["doctor"])
    assert "HarnessOps update path available" in first.stderr
    assert f"repo managed artifacts: {__version__}" in first.stderr
    assert f"current hops runtime:   {__version__}" in first.stderr
    assert "latest PyPI release:    99.0.0" in first.stderr
    assert "uvx --refresh-package harnessops --from harnessops hops update-harness --agent-bridge" in first.stderr

    cache = json.loads((root / ".harnessops" / "cache" / "update-notice.json").read_text(encoding="utf-8"))
    assert cache["latest_harnessops_version"] == "99.0.0"

    second = run_cli(["doctor"])
    assert "HarnessOps update path available" not in second.stderr


def test_update_notice_uses_pep440_version_ordering():
    assert update_notice._is_older("0.1.8rc1", "0.1.8")
    assert update_notice._is_older("0.1.8.dev0", "0.1.8")
    assert update_notice._is_older("0.1.8", "0.1.8.post1")
    assert not update_notice._is_older("0.1.8", "0.1.8rc1")


def test_update_notice_retries_pypi_after_short_failure_backoff(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    monkeypatch.delenv("HOPS_DISABLE_PYPI_UPDATE_CHECK", raising=False)
    calls = 0

    def fail_fetch():
        nonlocal calls
        calls += 1
        return None

    monkeypatch.setattr(update_notice, "_fetch_latest_pypi_version", fail_fetch)
    run_cli(["init", "--profile", "runops-project"])
    lock_path = root / ".harnessops" / "lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["harnessops_version"] = "0.0.1"
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    first = run_cli(["doctor"])
    assert "latest PyPI release:    unknown" in first.stderr
    assert calls == 1
    cache_path = root / ".harnessops" / "cache" / "update-notice.json"
    cache = json.loads(cache_path.read_text(encoding="utf-8"))
    assert "last_pypi_failure_at" in cache
    assert "last_pypi_success_at" not in cache

    run_cli(["report"])
    assert calls == 1

    cache["last_pypi_failure_at"] = (
        dt.datetime.now(dt.timezone.utc) - update_notice.PYPI_FAILURE_CHECK_INTERVAL - dt.timedelta(seconds=1)
    ).isoformat()
    cache_path.write_text(json.dumps(cache, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    run_cli(["report"])
    assert calls == 2


def test_update_notice_handles_unreleased_runtime_ahead_of_pypi(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    monkeypatch.delenv("HOPS_DISABLE_PYPI_UPDATE_CHECK", raising=False)
    monkeypatch.setattr(update_notice, "__version__", "99.0.0")
    monkeypatch.setattr(update_notice, "_fetch_latest_pypi_version", lambda: "0.1.7")

    run_cli(["init", "--profile", "runops-project"])
    lock_path = root / ".harnessops" / "lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["harnessops_version"] = "0.1.7"
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    first = run_cli(["doctor"])
    assert "current hops runtime:   99.0.0" in first.stderr
    assert "current hops runtime is newer than the latest PyPI release" in first.stderr
    assert "hops update-harness --agent-bridge" in first.stderr
    assert "uvx --refresh-package harnessops --from harnessops hops update-harness --agent-bridge" not in first.stderr


def test_update_notice_warns_when_repo_lock_is_newer_than_runtime(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    monkeypatch.delenv("HOPS_DISABLE_PYPI_UPDATE_CHECK", raising=False)
    monkeypatch.setattr(update_notice, "_fetch_latest_pypi_version", lambda: "0.1.7")

    run_cli(["init", "--profile", "runops-project"])
    lock_path = root / ".harnessops" / "lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["harnessops_version"] = "99.0.0"
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    first = run_cli(["doctor"])
    assert "repo managed artifacts: 99.0.0" in first.stderr
    assert "last updated by a newer HarnessOps runtime" in first.stderr
    assert "latest PyPI release is older than this repo's managed artifacts" in first.stderr
    assert "uvx --from harnessops==99.0.0 hops update-harness --agent-bridge" in first.stderr
    assert "uvx --refresh-package harnessops --from harnessops hops update-harness --agent-bridge" not in first.stderr


def test_update_notice_can_be_disabled_with_harnessops_env_alias(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    monkeypatch.setenv("HARNESSOPS_DISABLE_UPDATE_NOTICE", "1")

    run_cli(["init", "--profile", "runops-project"])
    lock_path = root / ".harnessops" / "lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["harnessops_version"] = "0.0.1"
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result = run_cli(["doctor"])
    assert "HarnessOps update path available" not in result.stderr


def test_update_harness_command_suppresses_stale_lock_notice(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)

    run_cli(["init", "--profile", "runops-project"])
    lock_path = root / ".harnessops" / "lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["harnessops_version"] = "0.0.1"
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result = run_cli(["update-harness"])
    assert "HarnessOps update path available" not in result.stderr


def test_update_notice_can_be_disabled_globally(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)

    run_cli(["init", "--profile", "runops-project"])
    lock_path = root / ".harnessops" / "lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["harnessops_version"] = "0.0.1"
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result = run_cli(["--disable-update-notice", "doctor"])
    assert "HarnessOps update path available" not in result.stderr
    assert not (root / ".harnessops" / "cache" / "update-notice.json").exists()


def test_update_harness_preserves_dynamic_imported_feedback_view(copy_fixture, monkeypatch):
    root = copy_fixture("paper-harness-upstream-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "paper-harness-upstream"])

    run_cli(["feedback", "import", "--issue", "1"])
    before = (root / "harness-lab/views/imported-feedback.md").read_text(encoding="utf-8")
    assert "FB0001" in before

    run_cli(["update-harness"])

    after = (root / "harness-lab/views/imported-feedback.md").read_text(encoding="utf-8")
    assert "FB0001" in after
    doctor = run_cli(["doctor", "--check-overlay", "--check-records"])
    assert "警告" not in doctor.output


def test_lab_refresh_views_repairs_all_managed_lab_artifact_warnings(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])
    run_cli(
        [
            "lab",
            "research-scan",
            "--title",
            "Refresh generated views",
            "--scope",
            "harnessops-core generated views",
            "--capability",
            "generated_view_management",
            "--failure-class",
            "stale_generated_view_repair_gap",
            "--candidate",
            "Refresh all managed lab artifacts|extends|propose|hops lab new-eval-case --from FB0001",
            "--recommendation",
            "repair stale generated view warnings.",
        ]
    )

    lock_path = root / ".harnessops/lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    for rel in [
        "harness-lab/README.md",
        "harness-lab/views/backlog.md",
        "harness-lab/views/score-trajectory.md",
    ]:
        lock["managed_files"][rel] = "sha256:stale"
    lock_path.write_text(json.dumps(lock, ensure_ascii=False, indent=2), encoding="utf-8")

    stale = run_cli(["doctor", "--check-overlay", "--check-records"])
    assert "harness-lab/README.md" in stale.output
    assert "harness-lab/views/backlog.md" in stale.output
    assert "harness-lab/views/score-trajectory.md" in stale.output

    refreshed = run_cli(["lab", "refresh-views"])

    assert "harness-lab/views/research-scans.md" in refreshed.output
    assert "RS0001" in (root / "harness-lab/views/research-scans.md").read_text(encoding="utf-8")
    doctor = run_cli(["doctor", "--check-overlay", "--check-records"])
    assert "警告" not in doctor.output


def test_feedback_import_issue_captures_github_context(copy_fixture, monkeypatch):
    root = copy_fixture("paper-harness-upstream-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "paper-harness-upstream"])

    payload = {
        "number": 42,
        "title": "Import records should include issue context",
        "body": "日本語の本文でも lab evaluation に必要な context を保持する。",
        "author": {"login": "alice"},
        "labels": [{"name": "enhancement"}, {"name": "feedback"}],
        "createdAt": "2026-05-12T01:02:03Z",
        "updatedAt": "2026-05-12T04:05:06Z",
        "url": "https://github.com/example/repo/issues/42",
        "comments": [
            {
                "author": {"login": "bob"},
                "createdAt": "2026-05-12T04:00:00Z",
                "body": "A useful follow-up comment with 日本語.",
            }
        ],
    }

    def fake_run(args, check, capture_output, text, encoding=None, errors=None):
        assert args[:4] == ["gh", "issue", "view", "42"]
        assert check is True
        assert capture_output is True
        assert text is True
        assert encoding == "utf-8"
        assert errors == "replace"
        return subprocess.CompletedProcess(args=args, returncode=0, stdout=json.dumps(payload), stderr="")

    monkeypatch.setattr(feedback_cli.subprocess, "run", fake_run)

    imported = run_cli(["feedback", "import", "--issue", "42", "--repo", "example/repo"])
    frontmatter, body = read_record(root / imported.output.strip())

    issue = frontmatter["source"]["issue"]
    assert issue["title"] == "Import records should include issue context"
    assert issue["author"] == "alice"
    assert issue["labels"] == ["enhancement", "feedback"]
    assert frontmatter["links"]["issue_url"] == "https://github.com/example/repo/issues/42"
    assert "日本語の本文" in body
    assert "A useful follow-up comment with 日本語" in body


def test_lab_capture_records_local_improvement(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])

    captured = run_cli(
        [
            "lab",
            "capture",
            "--title",
            "Local improvements were not captured in lab",
            "--summary",
            "HarnessOps changes could be implemented and released without a harness-lab record.",
            "--reproduction",
            "Implement a nontrivial CLI or skill change without an existing issue or feedback bundle.",
            "--expected-change",
            "Provide a first-class command to capture local improvement work before evaluation.",
            "--capability",
            "harness_lab_traceability",
            "--failure-class",
            "missing_lab_capture",
        ]
    )

    feedback_path = root / captured.output.strip()
    frontmatter, body = read_record(feedback_path)
    assert frontmatter["record_type"] == "imported_feedback"
    assert frontmatter["source"]["type"] == "local-capture"
    assert frontmatter["classification"]["capability"] == "harness_lab_traceability"
    assert "期待する上流変更" in body

    eval_case = run_cli(["lab", "new-eval-case", "--from", "FB0001"])
    eval_text = (root / eval_case.output.strip()).read_text(encoding="utf-8")
    assert "Provide a first-class command to capture local improvement work before evaluation." in eval_text
    assert "harness_lab_traceability" in eval_text
    doctor = run_cli(["doctor", "--check-overlay", "--check-records"])
    assert "警告" not in doctor.output


def test_lab_dossier_creates_single_improvement_file(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])

    empty = run_cli(["lab", "memory", "lint", "--max-files", "0"])
    assert "status: ok" in empty.output

    run_cli(
        [
            "lab",
            "capture",
            "--title",
            "Bridge workflow is hard to scan",
            "--summary",
            "A single improvement is spread across feedback, eval, hypothesis, and decision records.",
            "--expected-change",
            "Provide a generated dossier that gathers the normalized records into one review file.",
            "--capability",
            "lab_traceability",
            "--failure-class",
            "record_sprawl",
            "--source-ref",
            "https://github.com/example/harness/issues/7",
        ]
    )
    run_cli(["lab", "new-eval-case", "--from", "FB0001"])
    run_cli(["eval", "--case", "E0001", "--manual", "--score", "impact=4", "--notes", "Manual score is the review evidence."])
    run_cli(["propose", "--from", "E0001", "--hypothesis", "A generated dossier makes the improvement reviewable."])

    result = run_cli(["lab", "dossier", "--from", "H0001"])

    dossier_path = root / result.output.strip()
    assert dossier_path.name.startswith("IMP0001-")
    text = dossier_path.read_text(encoding="utf-8")
    assert "## Source Observation" in text
    assert "## Evaluation" in text
    assert "## Hypotheses" in text
    assert "## フィクスチャ" not in text
    assert "manual_eval_yml: `harness-lab/views/eval-results/E0001-manual-score.yml`" in text
    assert "scores: impact=4" in text
    assert "Manual score is the review evidence." in text
    assert "FB0001" in text
    assert "E0001" in text
    assert "H0001" in text
    view = (root / "harness-lab/views/improvements.md").read_text(encoding="utf-8")
    assert "IMP0001" in view
    assert "source=FB0001" in view

    run_cli(
        [
            "lab",
            "investigate",
            "--from",
            "IMP0001",
            "--kind",
            "external-benchmark",
            "--summary",
            "Compared with an external improvement loop and found investigation should be explicit.",
            "--evidence-ref",
            "docs/design-principles.md",
        ]
    )
    classified = run_cli(
        [
            "lab",
            "classify",
            "--from",
            "IMP0001",
            "--source-type",
            "friction",
            "--scope",
            "harnessops-core",
            "--maturity",
            "investigated",
            "--relation",
            "extends",
            "--promotion-level",
            "target-lab-case",
            "--guard-status",
            "planned",
            "--guard-path",
            "tests/test_cli/test_mvp_flow.py",
        ]
    )
    frontmatter, updated_text = read_record(root / classified.output.strip())
    assert frontmatter["source_type"] == "friction"
    assert frontmatter["maturity"] == "investigated"
    assert frontmatter["relation"] == "extends"
    assert frontmatter["guard"]["status"] == "planned"
    assert frontmatter["investigation"][0]["kind"] == "external-benchmark"
    assert "## Investigation" in updated_text
    assert "Compared with an external improvement loop" in updated_text
    assert "evidence: docs/design-principles.md" in updated_text
    view = (root / "harness-lab/views/improvements.md").read_text(encoding="utf-8")
    assert "maturity=investigated" in view
    assert "promotion=target-lab-case" in view

    second = run_cli(["lab", "dossier", "--from", "FB0001"])

    assert second.output.strip() == result.output.strip()


def test_lab_research_scan_records_structured_candidates(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])

    result = run_cli(
        [
            "lab",
            "research-scan",
            "--title",
            "Structure meta improvement research scan outputs",
            "--scope",
            "harnessops-core meta improvement research",
            "--capability",
            "meta_improvement_research",
            "--failure-class",
            "unstructured_research_scan_results",
            "--existing-dossier",
            "IMP0009",
            "--local-evidence",
            "Dry run produced useful candidates only in chat prose|harness-lab/improvements/IMP0009.md",
            "--codebase-evidence",
            "Research skill asks for candidates but has no structured artifact command|.agents/skills/hops-research-improvements/SKILL.md",
            "--external-benchmark",
            "Postmortem and experiment practices preserve structured action items and learning|https://sre.google/workbook/postmortem-culture/",
            "--risk",
            "Too many speculative records would create meta-noise|docs/design-principles.md",
            "--candidate",
            "Add research scan record|extends|propose|hops lab new-eval-case --from FB0001",
            "--recommendation",
            "propose structured research scan support before converting candidates to lab actions.",
        ]
    )

    scan_path = root / result.output.strip()
    frontmatter, body = read_record(scan_path)
    assert frontmatter["id"] == "RS0001"
    assert frontmatter["record_type"] == "research_scan"
    assert frontmatter["classification"]["capability"] == "meta_improvement_research"
    assert frontmatter["evidence"]["codebase"][0]["ref"] == ".agents/skills/hops-research-improvements/SKILL.md"
    assert frontmatter["candidates"][0]["relation"] == "extends"
    assert frontmatter["candidates"][0]["next_command"] == "hops lab new-eval-case --from FB0001"
    assert "## Candidates" in body
    assert "| Add research scan record | extends | propose | hops lab new-eval-case --from FB0001 |" in body
    assert "## Next Commands" in body

    view = (root / "harness-lab/views/research-scans.md").read_text(encoding="utf-8")
    assert "RS0001" in view
    assert "meta_improvement_research unstructured_research_scan_results" in view
    doctor = run_cli(["doctor", "--check-overlay", "--check-records"])
    assert "警告" not in doctor.output


def test_lab_compact_force_writes_mutable_knowledge(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])
    run_cli(
        [
            "lab",
            "capture",
            "--title",
            "Lab records need compaction",
            "--summary",
            "Long-running lab records need a compact knowledge layer.",
            "--expected-change",
            "Compile canonical records into source-linked mutable knowledge.",
            "--capability",
            "lab_memory_compaction",
            "--failure-class",
            "record_sprawl_without_knowledge_consolidation",
        ]
    )
    run_cli(["lab", "new-eval-case", "--from", "FB0001"])
    run_cli(["eval", "--case", "E0001", "--manual", "--score", "impact=4", "--notes", "Compaction keeps recurring lessons visible."])
    run_cli(
        [
            "propose",
            "--from",
            "E0001",
            "--hypothesis",
            "Mutable lab knowledge preserves lessons without replacing records.",
        ]
    )
    run_cli(["lab", "dossier", "--from", "H0001"])
    run_cli(
        [
            "lab",
            "classify",
            "--from",
            "IMP0001",
            "--guard-status",
            "planned",
            "--guard-path",
            "tests/test_cli/test_mvp_flow.py",
        ]
    )

    result = run_cli(["lab", "compact", "--force"])

    assert "status: written" in result.output
    assert "harness-lab/knowledge/lab-memory.yml" in result.output
    data = yamlio.safe_load((root / "harness-lab/knowledge/lab-memory.yml").read_text(encoding="utf-8"))
    assert data["kind"] == "harness_lab_knowledge"
    assert data["mutable"] is True
    capability = data["knowledge"]["capabilities"][0]
    assert capability["capability"] == "lab_memory_compaction"
    failure = capability["failure_classes"][0]
    assert failure["failure_class"] == "record_sprawl_without_knowledge_consolidation"
    assert failure["average_scores"]["impact"] == 4.0
    assert failure["guards"][0]["path"] == "tests/test_cli/test_mvp_flow.py"
    assert "Compaction keeps recurring lessons visible." in failure["lessons"][0]["lesson"]

    markdown_path = root / "harness-lab/knowledge/lab-memory.md"
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "## Curator Notes" in markdown
    markdown_path.write_text(
        markdown.replace(
            "ここは `hops lab compact` が保持する手編集領域です。",
            "Keep this manually curated note.",
        ),
        encoding="utf-8",
    )
    run_cli(["lab", "compact", "--force"])
    assert "Keep this manually curated note." in markdown_path.read_text(encoding="utf-8")
    doctor = run_cli(["doctor", "--check-overlay", "--check-records"])
    assert "警告" not in doctor.output


def test_lab_compact_skips_until_threshold(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])

    skipped = run_cli(
        [
            "lab",
            "compact",
            "--max-files",
            "9999",
            "--max-bytes",
            "999999999",
            "--max-improvements",
            "9999",
        ]
    )

    assert "status: skipped" in skipped.output
    assert not (root / "harness-lab/knowledge/lab-memory.yml").exists()

    written = run_cli(["lab", "compact", "--max-files", "0"])

    assert "status: written" in written.output
    assert "file_count>0" in written.output
    assert (root / "harness-lab/knowledge/lab-memory.yml").exists()


def test_lab_memory_lint_and_prepare_abstraction_input(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])
    run_cli(
        [
            "lab",
            "capture",
            "--title",
            "Lab memory needs semantic abstraction",
            "--summary",
            "A deterministic snapshot helps lookup, but recurring lessons need a skill-curated abstraction.",
            "--expected-change",
            "Provide lint triggers and a source bundle for an abstraction skill.",
            "--capability",
            "lab_memory_compaction",
            "--failure-class",
            "snapshot_without_semantic_abstraction",
        ]
    )
    run_cli(["lab", "dossier", "--from", "FB0001"])

    failed = runner.invoke(app, ["lab", "memory", "lint", "--max-files", "0"])

    assert failed.exit_code == 1
    assert "status: needs-abstraction" in failed.output
    assert "file_count>0" in failed.output
    assert "semantic_memory_missing" in failed.output
    assert "hops lab memory prepare --force" in failed.output

    warned = run_cli(["lab", "memory", "lint", "--max-files", "0", "--warn-only"])

    assert "status: needs-abstraction" in warned.output

    prepared = run_cli(["lab", "memory", "prepare", "--force"])

    assert "status: written" in prepared.output
    assert "harness-lab/knowledge/lab-memory-input.yml" in prepared.output
    data = yamlio.safe_load((root / "harness-lab/knowledge/lab-memory-input.yml").read_text(encoding="utf-8"))
    assert data["kind"] == "harness_lab_memory_abstraction_input"
    assert data["lint"]["source_digest"]
    assert data["sources"][0]["id"] == "IMP0001"
    assert data["abstraction_targets"][0]["path"] == "harness-lab/knowledge/principles.md"
    assert data["abstraction_manifest_template"]["kind"] == "harness_lab_memory_abstraction"
    markdown = (root / "harness-lab/knowledge/lab-memory-input.md").read_text(encoding="utf-8")
    assert "## Skill Instructions" in markdown
    assert "hops-compact-lab-memory" in markdown
    doctor = run_cli(["doctor", "--check-overlay", "--check-records"])
    assert "警告" not in doctor.output


def test_parallel_lab_dossier_creation_is_source_feedback_idempotent(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])
    run_cli(
        [
            "lab",
            "capture",
            "--title",
            "Concurrent dossier calls duplicate records",
            "--summary",
            "Parallel lab commands should not create two dossiers for one feedback record.",
            "--expected-change",
            "Dossier creation is source-feedback-idempotent.",
        ]
    )
    project = load_project(root)

    with ThreadPoolExecutor(max_workers=4) as executor:
        paths = list(executor.map(lambda _: create_or_update_improvement_dossier(project, source_ref="FB0001"), range(4)))

    assert {path.name for path in paths} == {paths[0].name}
    assert len(list((root / "harness-lab/improvements").glob("IMP*.md"))) == 1


def test_doctor_rejects_duplicate_improvement_dossier_source_feedback(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])
    run_cli(
        [
            "lab",
            "capture",
            "--title",
            "Duplicate source feedback",
            "--summary",
            "Duplicate improvement dossiers should be detected.",
            "--expected-change",
            "Doctor reports duplicate source_feedback mappings.",
        ]
    )
    result = run_cli(["lab", "dossier", "--from", "FB0001"])
    dossier_path = root / result.output.strip()
    frontmatter, body = read_record(dossier_path)
    frontmatter["id"] = "IMP0002"
    duplicate_path = root / "harness-lab/improvements/IMP0002-duplicate-source-feedback.md"
    duplicate_path.write_text(dump_record(frontmatter, body), encoding="utf-8")

    doctor = runner.invoke(app, ["doctor", "--check-overlay", "--check-records"])

    assert doctor.exit_code == 1
    assert "duplicate improvement dossier source_feedback FB0001" in doctor.output


def test_agent_user_install_is_removed(copy_fixture, tmp_path, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    monkeypatch.setenv("HOME", str(tmp_path))
    run_cli(["init", "--profile", "harnessops-core"])
    result = runner.invoke(app, ["agent", "install", "--codex", "--scope", "user"])
    assert result.exit_code == 1
    assert "user plugin install は廃止されました" in result.output
    assert not (tmp_path / ".codex/plugins/harnessops").exists()
    assert not (tmp_path / ".agents/plugins/marketplace.json").exists()


def test_eval_by_experiment_record(copy_fixture, monkeypatch):
    root = copy_fixture("runops-upstream-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-upstream"])
    experiment_dir = root / "harness-lab/records/experiments/X0001-example"
    experiment_dir.mkdir(parents=True)
    (experiment_dir / "experiment.md").write_text(
        """---
id: X0001
record_type: experiment
created_at: 2026-05-12T00:00:00+09:00
status: running
hypothesis: H0001
eval_cases:
  - E0001
---

# X0001: Example
""",
        encoding="utf-8",
    )
    eval_path = root / "harness-lab/records/eval-cases/E0001-example.md"
    eval_path.write_text(
        """---
id: E0001
record_type: eval_case
created_at: 2026-05-12T00:00:00+09:00
status: active
capability: routing
failure_class: routing_gap
source_feedback: FB0001
---

# E0001: Example

## フィクスチャ

fixture

## タスク

task

## 期待される挙動

expected

## 合格基準

- pass

## 不合格基準

- fail
""",
        encoding="utf-8",
    )

    result = run_cli(["eval", "--experiment", "X0001", "--manual", "--score", "impact=3"])

    assert "eval-results/E0001-manual-score.yml" in result.output
    eval_markdown = (root / "harness-lab/views/eval-results/E0001-manual-score.md").read_text(encoding="utf-8")
    assert "## 評価ケーススナップショット" not in eval_markdown
    assert "capability: routing" in eval_markdown


def test_eval_case_lookup_prefers_record_over_generated_eval_view(copy_fixture, monkeypatch):
    root = copy_fixture("runops-upstream-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-upstream"])
    eval_path = root / "harness-lab/records/eval-cases/E0001-example.md"
    eval_path.write_text(
        """---
id: E0001
record_type: eval_case
created_at: 2026-05-12T00:00:00+09:00
status: active
capability: routing
failure_class: routing_gap
source_feedback: FB0001
---

# E0001: Example

## フィクスチャ

fixture

## タスク

task

## 期待される挙動

expected

## 合格基準

- pass

## 不合格基準

- fail
""",
        encoding="utf-8",
    )

    run_cli(["eval", "--case", "E0001", "--manual", "--score", "impact=3"])
    second = run_cli(["eval", "--case", "E0001", "--manual", "--score", "impact=4"])

    assert "eval-results/E0001-manual-score.yml" in second.output
