import json

from typer.testing import CliRunner

from harnessops.cli.main import app
from harnessops.core.records import read_record


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
    assert (root / ".harnessops/lock.json").exists()
    assert (root / "harness-feedback/README.md").exists()
    assert (root / "harness-feedback/records/failures").is_dir()

    run_cli(["doctor", "--check-overlay", "--check-records"])
    run_cli(["migrate", "--check"])


def test_init_doctor_migrate_upstream(copy_fixture, monkeypatch):
    root = copy_fixture("runops-upstream-minimal")
    monkeypatch.chdir(root)

    run_cli(["init", "--profile", "runops-upstream"])
    assert (root / "harness-lab/README.md").exists()
    assert (root / "harness-lab/records/feedback").is_dir()
    run_cli(["doctor", "--check-overlay", "--check-records"])
    run_cli(["migrate", "--check"])


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
    assert "直接組み替えない" in text
    assert (root / ".agents/skills/hops-add-failure/SKILL.md").exists()
    assert (root / ".agents/skills/hops-issue-triage/SKILL.md").exists()
    assert (root / ".agents/skills/hops-update-harness/SKILL.md").exists()


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


def test_update_harness_can_add_repo_local_agent_bridge(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "runops-project"])

    run_cli(["update-harness", "--agent-bridge", "--codex"])

    assert (root / ".agents/skills/harnessops-bridge/SKILL.md").exists()
    assert (root / ".agents/skills/hops-update-harness/SKILL.md").exists()


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
    assert (root / eval_case.output.strip()).exists()
    doctor = run_cli(["doctor", "--check-overlay", "--check-records"])
    assert "警告" not in doctor.output


def test_agent_user_install_uses_home(copy_fixture, tmp_path, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    monkeypatch.setenv("HOME", str(tmp_path))
    run_cli(["init", "--profile", "harnessops-core"])
    result = run_cli(["agent", "install", "--codex", "--scope", "user"])
    assert ".codex/plugins/harnessops" in result.output
    assert ".agents/plugins/marketplace.json" in result.output
    assert (tmp_path / ".codex/plugins/harnessops/.codex-plugin/plugin.json").exists()
    marketplace = json.loads((tmp_path / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    entry = next(plugin for plugin in marketplace["plugins"] if plugin["name"] == "harnessops")
    assert entry["source"]["path"] == "./.codex/plugins/harnessops"
    assert entry["policy"]["installation"] == "AVAILABLE"


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
