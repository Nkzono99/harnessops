from typer.testing import CliRunner

from harnessops.cli.main import app


def test_cli_smoke_commands(copy_fixture, monkeypatch):
    root = copy_fixture("harnessops-core-minimal")
    monkeypatch.chdir(root)
    runner = CliRunner()
    for args in [
        ["version"],
        ["profiles", "list"],
        ["profiles", "show", "runops-project"],
        ["detect"],
        ["init", "--profile", "harnessops-core"],
        ["doctor"],
        ["migrate", "--check"],
        ["agent", "bridge", "--codex"],
        ["agent", "verify"],
    ]:
        result = runner.invoke(app, args)
        assert result.exit_code == 0, (args, result.output)
