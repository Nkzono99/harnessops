import json

from typer.testing import CliRunner

from harnessops.cli.main import app
from harnessops.core.agent_asset_sync import sync_packaged_skill_assets


runner = CliRunner()


def _write(path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _asset_skill(root, host: str, name: str):
    return root / "src/harnessops/agent_assets/skills" / host / "harnessops/skills" / name / "SKILL.md"


def test_sync_packaged_skill_assets_updates_drift_and_retires_removed_skills(tmp_path):
    _write(tmp_path / ".agents/skills/hops-one/SKILL.md", "one\n")
    _write(_asset_skill(tmp_path, "codex", "hops-one"), "old\n")
    _write(_asset_skill(tmp_path, "claude", "hops-one"), "old\n")
    _write(_asset_skill(tmp_path, "codex", "hops-extra"), "extra\n")

    checked = sync_packaged_skill_assets(tmp_path, check=True)

    assert checked["ok"] is False
    assert "src/harnessops/agent_assets/skills/codex/harnessops/skills/hops-one/SKILL.md" in checked["drifted"]
    assert "src/harnessops/agent_assets/skills/claude/harnessops/skills/hops-one/SKILL.md" in checked["drifted"]
    assert "src/harnessops/agent_assets/skills/codex/harnessops/skills/hops-extra" in checked["retired"]
    assert _asset_skill(tmp_path, "codex", "hops-one").read_text(encoding="utf-8") == "old\n"

    synced = sync_packaged_skill_assets(tmp_path)

    assert synced["ok"] is True
    assert _asset_skill(tmp_path, "codex", "hops-one").read_text(encoding="utf-8") == "one\n"
    assert _asset_skill(tmp_path, "claude", "hops-one").read_text(encoding="utf-8") == "one\n"
    assert not _asset_skill(tmp_path, "codex", "hops-extra").exists()
    assert sync_packaged_skill_assets(tmp_path, check=True)["ok"] is True


def test_agent_sync_packaged_skills_cli_check_reports_drift(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write(tmp_path / ".agents/skills/hops-one/SKILL.md", "one\n")
    _write(_asset_skill(tmp_path, "codex", "hops-one"), "old\n")
    _write(_asset_skill(tmp_path, "claude", "hops-one"), "one\n")

    result = runner.invoke(app, ["agent", "sync-packaged-skills", "--check", "--json"])

    assert result.exit_code == 1
    payload = json.loads(result.output)
    assert payload["ok"] is False
    assert payload["check"] is True
    assert payload["drifted"] == [
        "src/harnessops/agent_assets/skills/codex/harnessops/skills/hops-one/SKILL.md"
    ]
