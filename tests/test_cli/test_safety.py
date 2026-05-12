from typer.testing import CliRunner

from harnessops.cli.main import app


runner = CliRunner()


def test_init_refuses_to_overwrite_user_edited_generated_file(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    readme = root / "harness-feedback/README.md"
    readme.write_text("# human edit\n", encoding="utf-8")

    result = runner.invoke(app, ["init", "--profile", "runops-project"])

    assert result.exit_code == 2
    assert readme.read_text(encoding="utf-8") == "# human edit\n"


def test_feedback_export_refuses_unsanitized_by_default(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    assert runner.invoke(app, ["add-failure", "--title", "Harness update missed", "--target", "runops"]).exit_code == 0

    result = runner.invoke(app, ["feedback", "export", "--target", "runops"])

    assert result.exit_code == 1
    assert "refusing unsanitized export" in result.output


def test_add_failure_rejects_invalid_disposition(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0

    result = runner.invoke(app, ["add-failure", "--title", "bad", "--disposition", "not-a-disposition"])

    assert result.exit_code == 1
    assert "invalid disposition" in result.output
    assert not list((root / "harness-feedback/records/failures").glob("F*.md"))


def test_feedback_export_skips_project_evolution(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    assert runner.invoke(
        app,
        [
            "add-failure",
            "--title",
            "research pivot only",
            "--target",
            "runops",
            "--disposition",
            "project-evolution",
        ],
    ).exit_code == 0

    result = runner.invoke(app, ["feedback", "export", "--target", "runops", "--sanitize"])

    assert result.exit_code == 1
    assert "no matching feedback records" in result.output


def test_feedback_import_rejects_unsanitized_markdown(copy_fixture, tmp_path, monkeypatch):
    root = copy_fixture("runops-upstream-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-upstream"]).exit_code == 0
    bad = tmp_path / "README.md"
    bad.write_text("# Not feedback\n", encoding="utf-8")

    result = runner.invoke(app, ["feedback", "import", str(bad)])

    assert result.exit_code == 1
    assert "import requires" in result.output


def test_doctor_fails_pending_migration_unless_allowed(copy_fixture, monkeypatch):
    import json

    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    lock = root / ".harnessops/lock.json"
    data = json.loads(lock.read_text(encoding="utf-8"))
    data["layout_version"] = "9.9"
    lock.write_text(json.dumps(data), encoding="utf-8")

    failed = runner.invoke(app, ["doctor"])
    allowed = runner.invoke(app, ["doctor", "--allow-pending"])

    assert failed.exit_code == 1
    assert "pending migration" in failed.output
    assert allowed.exit_code == 0


def test_migrate_apply_normalizes_unsupported_layout(copy_fixture, monkeypatch):
    import json

    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    lock = root / ".harnessops/lock.json"
    data = json.loads(lock.read_text(encoding="utf-8"))
    data["layout_version"] = "9.9"
    lock.write_text(json.dumps(data), encoding="utf-8")

    result = runner.invoke(app, ["migrate", "--apply"])

    assert result.exit_code == 0
    assert json.loads(lock.read_text(encoding="utf-8"))["layout_version"] == "0.1"
    assert list((root / ".harnessops/migrations").glob("9.9-to-0.1.md"))


def test_adopted_decision_requires_evidence_and_guard(copy_fixture, monkeypatch):
    root = copy_fixture("runops-upstream-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-upstream"]).exit_code == 0

    result = runner.invoke(app, ["decide", "--from", "H0001", "--status", "adopted"])

    assert result.exit_code == 1
    assert "adopted decisions require" in result.output


def test_sanitize_config_redacts_private_terms(copy_fixture, monkeypatch):
    root = copy_fixture("runops-project-minimal")
    monkeypatch.chdir(root)
    assert runner.invoke(app, ["init", "--profile", "runops-project"]).exit_code == 0
    sanitize_config = root / ".harnessops/sanitize.yml"
    sanitize_config.write_text("private_terms:\n  - secret-method\n", encoding="utf-8")
    assert runner.invoke(
        app,
        [
            "add-failure",
            "--title",
            "Secret method leaked",
            "--target",
            "runops",
            "--context",
            "secret-method appeared in public output",
        ],
    ).exit_code == 0

    result = runner.invoke(app, ["feedback", "export", "--sanitize"])

    assert result.exit_code == 0
    exported = root / result.output.strip()
    assert "secret-method" not in exported.read_text(encoding="utf-8")
