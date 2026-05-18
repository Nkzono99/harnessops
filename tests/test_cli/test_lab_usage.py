from __future__ import annotations

import json

from typer.testing import CliRunner

from harnessops.cli.main import app
from harnessops.core import yamlio
from harnessops.core.record_io import read_record


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
    run_cli(["lab", "eval-case", "create", "--from", "FB0001"])
    run_cli(
        [
            "lab",
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
            "Add lab context command|extends|propose|hops lab new-eval-case --from FB0001",
            "--recommendation",
            "Use context before implementation.",
        ]
    )


def test_lab_queue_ranks_recorded_work(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])
    _seed_lab_queue()

    result = run_cli(["lab", "review", "queue", "--json"])
    payload = json.loads(result.output)

    assert payload["kind"] == "harness_lab_queue"
    assert payload["count"] >= 2
    first = payload["items"][0]
    assert first["id"] == "IMP0001"
    assert "manual-eval-needed" in first["reasons"]
    assert "decision-needed" in first["reasons"]
    assert "hops lab eval --case E0001 --manual" in first["next_command"]
    research_item = next(item for item in payload["items"] if item["id"] == "RS0001")
    assert research_item["next_command"] == "hops lab eval-case create --from FB0001"


def test_lab_context_returns_related_records_and_reads(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])
    _seed_lab_queue()
    run_cli(["lab", "memory", "compact", "--force"])

    result = run_cli(["lab", "review", "context", "--capability", "lab_reuse", "--json"])
    payload = json.loads(result.output)

    assert payload["kind"] == "harness_lab_context"
    assert payload["related_improvements"][0]["id"] == "IMP0001"
    assert payload["research_scans"][0]["id"] == "RS0001"
    assert payload["knowledge"]["available"] is True
    assert any(path.startswith("harness-lab/improvements/IMP0001-") for path in payload["recommended_reads"])


def test_lab_retire_preserves_record_and_excludes_active_queue_and_memory(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])
    run_cli(
        [
            "lab",
            "research-scan",
            "--title",
            "Retire stale candidate",
            "--scope",
            "harnessops-core",
            "--capability",
            "lab_memory_compaction",
            "--failure-class",
            "source_preserving_queue_retirement_gap",
            "--candidate",
            "Close obsolete issue|parks|park|gh issue close 123",
            "--recommendation",
            "Retire when the source issue is already closed.",
        ]
    )

    queued = json.loads(run_cli(["lab", "review", "queue", "--json"]).output)
    assert any(item["id"] == "RS0001" for item in queued["items"])

    retired = json.loads(
        run_cli(
            [
                "lab",
                "retire",
                "--from",
                "RS0001",
                "--reason",
                "source issue already closed",
                "--evidence-ref",
                "gh issue list --state all",
                "--json",
            ]
        ).output
    )
    record_path = root / retired["path"]
    frontmatter, _ = read_record(record_path)
    assert record_path.exists()
    assert frontmatter["status"] == "archived"
    assert frontmatter["retirement"][0]["reason"] == "source issue already closed"

    active_queue = json.loads(run_cli(["lab", "review", "queue", "--json"]).output)
    assert all(item["id"] != "RS0001" for item in active_queue["items"])
    closed_queue = json.loads(run_cli(["lab", "review", "queue", "--include-closed", "--json"]).output)
    assert any(item["id"] == "RS0001" and item["status"] == "archived" for item in closed_queue["items"])
    context = json.loads(
        run_cli(["lab", "review", "context", "--capability", "lab_memory_compaction", "--json"]).output
    )
    assert all(item["id"] != "RS0001" for item in context["research_scans"])

    run_cli(["lab", "memory", "prepare", "--force"])
    memory_input = yamlio.safe_load((root / "harness-lab/knowledge/lab-memory-input.yml").read_text(encoding="utf-8"))
    assert "RS0001" not in {source["id"] for source in memory_input["sources"]}


def test_lab_lifecycle_lint_reports_actionable_gaps(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    run_cli(["init", "--profile", "harnessops-core"])
    _seed_lab_queue()

    result = run_cli(["lab", "review", "lint", "--json"])
    payload = json.loads(result.output)

    assert payload["kind"] == "harness_lab_lifecycle_lint"
    assert payload["status"] == "warning"
    codes = {item["code"] for item in payload["issues"]}
    assert "manual-eval-missing" in codes
    assert "decision-missing" in codes
    assert "research-candidates-present" in codes
