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

