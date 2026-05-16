from __future__ import annotations

import json

from typer.testing import CliRunner

from harnessops.cli.main import app


runner = CliRunner()


def run_cli(args):
    result = runner.invoke(app, args)
    assert result.exit_code == 0, result.output
    return result


def _seed_lab_queue() -> None:
    run_cli(
        [
            "lab",
            "capture",
            "--title",
            "Lab records need retrieval",
            "--summary",
            "Records are captured but not reused before implementation.",
            "--expected-change",
            "Expose ranked queue and contextual recall commands.",
            "--capability",
            "lab_reuse",
            "--failure-class",
            "records_without_reuse_path",
        ]
    )
    run_cli(["lab", "new-eval-case", "--from", "FB0001"])
    run_cli(
        [
            "propose",
            "--from",
            "E0001",
            "--hypothesis",
            "A queue command makes priority work explicit.",
        ]
    )
    run_cli(["lab", "dossier", "--from", "H0001"])
    run_cli(
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
            "hypothesis",
            "--relation",
            "extends",
            "--guard-status",
            "planned",
            "--guard-path",
            "tests/test_cli/test_lab_usage.py",
        ]
    )
    run_cli(
        [
            "lab",
            "research-scan",
            "--title",
            "Context command should reuse old decisions",
            "--scope",
            "harnessops-core",
            "--capability",
            "lab_reuse",
            "--failure-class",
            "records_without_reuse_path",
            "--existing-dossier",
            "IMP0001",
            "--candidate",
            "Add lab context command|extends|propose|hops lab context --capability lab_reuse",
            "--recommendation",
            "Use context before implementation.",
        ]
    )


def test_lab_queue_ranks_recorded_work(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])
    _seed_lab_queue()

    result = run_cli(["lab", "queue", "--json"])
    payload = json.loads(result.output)

    assert payload["kind"] == "harness_lab_queue"
    assert payload["count"] >= 2
    first = payload["items"][0]
    assert first["id"] == "IMP0001"
    assert "manual-eval-needed" in first["reasons"]
    assert "decision-needed" in first["reasons"]
    assert "hops eval --case E0001 --manual" in first["next_command"]
    assert any(item["id"] == "RS0001" for item in payload["items"])


def test_lab_context_returns_related_records_and_reads(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])
    _seed_lab_queue()
    run_cli(["lab", "compact", "--force"])

    result = run_cli(["lab", "context", "--capability", "lab_reuse", "--json"])
    payload = json.loads(result.output)

    assert payload["kind"] == "harness_lab_context"
    assert payload["related_improvements"][0]["id"] == "IMP0001"
    assert payload["research_scans"][0]["id"] == "RS0001"
    assert payload["knowledge"]["available"] is True
    assert any(path.startswith("harness-lab/improvements/IMP0001-") for path in payload["recommended_reads"])


def test_lab_lifecycle_lint_reports_actionable_gaps(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])
    _seed_lab_queue()

    result = run_cli(["lab", "lifecycle", "lint", "--json"])
    payload = json.loads(result.output)

    assert payload["kind"] == "harness_lab_lifecycle_lint"
    assert payload["status"] == "warning"
    codes = {item["code"] for item in payload["issues"]}
    assert "manual-eval-missing" in codes
    assert "decision-missing" in codes
    assert "research-candidates-present" in codes
