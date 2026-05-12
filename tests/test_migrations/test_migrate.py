from typer.testing import CliRunner

from harnessops.cli.main import app


def test_migrate_check_after_fresh_init(copy_fixture, monkeypatch):
    root = copy_fixture("paper-project-minimal")
    monkeypatch.chdir(root)
    runner = CliRunner()
    assert runner.invoke(app, ["init", "--profile", "paper-harness-project"]).exit_code == 0
    result = runner.invoke(app, ["migrate", "--check", "--json"])
    assert result.exit_code == 0
    assert '"ok": true' in result.output

