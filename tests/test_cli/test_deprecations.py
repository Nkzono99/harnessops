from __future__ import annotations

from typer.testing import CliRunner

from harnessops.cli.main import app


runner = CliRunner()


def test_legacy_feedback_commands_warn_but_canonical_commands_do_not(copy_fixture, monkeypatch) -> None:
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0

    legacy = runner.invoke(
        app,
        ["add-failure", "--title", "Legacy capture", "--target", "runops"],
    )

    assert legacy.exit_code == 0, legacy.output
    assert "DEPRECATED: `add-failure` is deprecated; use `hops feedback add-failure`." in legacy.stderr

    canonical = runner.invoke(
        app,
        ["feedback", "add-failure", "--title", "Canonical capture", "--target", "runops"],
    )

    assert canonical.exit_code == 0, canonical.output
    assert "DEPRECATED" not in canonical.stderr


def test_legacy_lab_review_commands_warn_but_canonical_commands_do_not(copy_fixture, monkeypatch) -> None:
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "harnessops-core"]).exit_code == 0

    legacy = runner.invoke(app, ["lab", "queue", "--json"])

    assert legacy.exit_code == 0, legacy.output
    assert "DEPRECATED: `lab queue` is deprecated; use `hops lab review queue`." in legacy.stderr

    canonical = runner.invoke(app, ["lab", "review", "queue", "--json"])

    assert canonical.exit_code == 0, canonical.output
    assert "DEPRECATED" not in canonical.stderr


def test_legacy_commands_are_hidden_from_help() -> None:
    top_help = runner.invoke(app, ["--help"])
    lab_help = runner.invoke(app, ["lab", "--help"])

    assert top_help.exit_code == 0
    assert lab_help.exit_code == 0
    assert "add-failure" not in top_help.output
    assert "add-feedback" not in top_help.output
    assert "route" not in top_help.output
    assert "new-eval-case" not in lab_help.output
    assert "lifecycle" not in lab_help.output
